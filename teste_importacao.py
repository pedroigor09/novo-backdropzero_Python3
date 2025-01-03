# teste_importacao.py
try:
    from skimage import io
    print("scikit-image importado com sucesso")
except ImportError:
    print("Falha ao importar scikit-image")
