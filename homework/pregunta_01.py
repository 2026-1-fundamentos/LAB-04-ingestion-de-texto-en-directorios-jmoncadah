# pylint: disable=import-outside-toplevel
# pylint: disable=line-too-long
# flake8: noqa
"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""
import zipfile
from pathlib import Path
import pandas as pd


def pregunta_01():
    """
    La información requerida para este laboratio esta almacenada en el
    archivo "files/input.zip" ubicado en la carpeta raíz.
    Descomprima este archivo.

    Como resultado se creara la carpeta "input" en la raiz del
    repositorio, la cual contiene la siguiente estructura de archivos:


    ```
    train/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    test/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    ```

    A partir de esta informacion escriba el código que permita generar
    dos archivos llamados "train_dataset.csv" y "test_dataset.csv". Estos
    archivos deben estar ubicados en la carpeta "output" ubicada en la raiz
    del repositorio.

    Estos archivos deben tener la siguiente estructura:

    * phrase: Texto de la frase. hay una frase por cada archivo de texto.
    * sentiment: Sentimiento de la frase. Puede ser "positive", "negative"
      o "neutral". Este corresponde al nombre del directorio donde se
      encuentra ubicado el archivo.

    Cada archivo tendria una estructura similar a la siguiente:

    ```
    |    | phrase                                                                                                                                                                 | target   |
    |---:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|
    |  0 | Cardona slowed her vehicle , turned around and returned to the intersection , where she called 911                                                                     | neutral  |
    |  1 | Market data and analytics are derived from primary and secondary research                                                                                              | neutral  |
    |  2 | Exel is headquartered in Mantyharju in Finland                                                                                                                         | neutral  |
    |  3 | Both operating profit and net sales for the three-month period increased , respectively from EUR16 .0 m and EUR139m , as compared to the corresponding quarter in 2006 | positive |
    |  4 | Tampere Science Parks is a Finnish company that owns , leases and builds office properties and it specialises in facilities for technology-oriented businesses         | neutral  |
    ```


    """
    # Rutas base
    zip_path = Path("files/input.zip")
    input_dir = Path("input")
    output_dir = Path("files/output")

    # Crear carpeta de salida si no existe
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Descomprimir el archivo si aún no existe la carpeta input
    if not input_dir.exists():
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall()

    # 2. Función para construir un dataset a partir de las carpetas
    def build_dataset(base_dir):
        phrases = []
        targets = []

        for sentiment_dir in base_dir.iterdir():
            if sentiment_dir.is_dir():
                target = sentiment_dir.name
                for txt_file in sentiment_dir.glob("*.txt"):
                    with open(txt_file, "r", encoding="utf-8") as f:
                        text = f.read().strip()
                    phrases.append(text)
                    targets.append(target)

        return pd.DataFrame({"phrase": phrases, "target": targets})

    # 3. Crear los datasets
    train_df = build_dataset(input_dir / "train")
    test_df = build_dataset(input_dir / "test")

    # 4. Guardar los CSVs en la carpeta de salida
    train_df.to_csv(output_dir / "train_dataset.csv", index=False)
    test_df.to_csv(output_dir / "test_dataset.csv", index=False)