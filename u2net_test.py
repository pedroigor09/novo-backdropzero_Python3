import os
import sys
from skimage import io
import torch
from torch.autograd import Variable
from torch.utils.data import DataLoader
from torchvision import transforms
import numpy as np
from PIL import Image

from data_loader import RescaleT, ToTensorLab, SalObjDataset
from model import U2NET, U2NETP

def normPRED(d):
    ma = torch.max(d)
    mi = torch.min(d)
    dn = (d - mi) / (ma - mi)
    return dn

def save_output(image_name, pred, d_dir):
    predict = pred
    predict = predict.squeeze()
    predict_np = predict.cpu().data.numpy()

    im = Image.fromarray((predict_np * 255).astype(np.uint8)).convert('L')
    img_name = image_name.split(os.sep)[-1]
    image = io.imread(image_name)
    imo = im.resize((image.shape[1], image.shape[0]), resample=Image.BILINEAR)

    pb_np = np.array(imo)

    # Cria uma máscara binária e a aplica na imagem original
    image = Image.fromarray(image).convert("RGBA")
    empty = Image.new("RGBA", image.size, 0)
    mask = Image.fromarray(pb_np).convert("L")
    output_image = Image.composite(image, empty, mask)

    aaa = img_name.split(".")
    bbb = aaa[0:-1]
    imidx = bbb[0]
    for i in range(1, len(bbb)):
        imidx = imidx + "." + bbb[i]

    output_path = os.path.join(d_dir, imidx + '.png')
    output_image.save(output_path)
    print(f"Imagem salva em: {output_path}")

def main(input_image):
    try:
        model_name = 'u2net'

        image_dir = os.path.join(os.getcwd(), 'test_data', 'test_images')
        prediction_dir = os.path.join(os.getcwd(), 'test_data', model_name + '_results')
        model_dir = os.path.join(os.getcwd(), 'saved_models', model_name, model_name + '.pth')

        img_name_list = [input_image]
        print(f"Lista de imagens: {img_name_list}")

        test_salobj_dataset = SalObjDataset(
            img_name_list=img_name_list,
            lbl_name_list=[],
            transform=transforms.Compose([RescaleT(320), ToTensorLab(flag=0)])
        )
        test_salobj_dataloader = DataLoader(test_salobj_dataset, batch_size=1, shuffle=False, num_workers=1)
        print("DataLoader configurado")

        if model_name == 'u2net':
            print("...load U2NET---173.6 MB")
            net = U2NET(3, 1)
        elif model_name == 'u2netp':
            print("...load U2NEP---4.7 MB")
            net = U2NETP(3, 1)

        if torch.cuda.is_available():
            net.load_state_dict(torch.load(model_dir))
            net.cuda()
        else:
            net.load_state_dict(torch.load(model_dir, map_location='cpu'))
        net.eval()
        print("Modelo carregado e configurado")

        for i_test, data_test in enumerate(test_salobj_dataloader):
            print(f"Inferenciando: {img_name_list[i_test].split(os.sep)[-1]}")

            inputs_test = data_test['image']
            inputs_test = inputs_test.type(torch.FloatTensor)

            if torch.cuda.is_available():
                inputs_test = Variable(inputs_test.cuda())
            else:
                inputs_test = Variable(inputs_test)

            d1, d2, d3, d4, d5, d6, d7 = net(inputs_test)

            pred = d1[:, 0, :, :]
            pred = normPRED(pred)

            if not os.path.exists(prediction_dir):
                os.makedirs(prediction_dir, exist_ok=True)
            save_output(img_name_list[i_test], pred, prediction_dir)

            del d1, d2, d3, d4, d5, d6, d7

        print("Processamento concluído com sucesso")
    except Exception as e:
        print(f"Erro no processamento da imagem: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python u2net_test.py <caminho_para_imagem>")
    else:
        main(sys.argv[1])
