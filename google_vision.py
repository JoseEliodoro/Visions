import os
import base64
import pickle
import pandas as pd
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "keys_google.json"

from typing import Sequence, List
from google.cloud import vision


def analyze_image_from_uri(
  image_uri: str,
  feature_types: Sequence,
) -> vision.AnnotateImageResponse:
  client = vision.ImageAnnotatorClient()
 
  """ 
  image = vision.Image()
  image.source.image_uri = image_uri 
  """
  with open(image_uri, "rb") as image_file:
    content = image_file.read()

  image = vision.Image(content=content)
  features = [vision.Feature(type_=feature_type) for feature_type in feature_types]
  request = vision.AnnotateImageRequest(image=image, features=features)

  response = client.annotate_image(request=request)

  return response

def create_row(lista: List, fileID: str, classe: str, subclass: str, percent: float) -> None:
  el = {
    'ID': fileID,
    'Class': classe,
    'Percent': round(percent, 2),
    'Subclass': subclass
  }
  if (el not in lista):
    lista.append(el)

def rows_data(response: vision.AnnotateImageResponse, fileID:str) -> List:
  rows = []
  # OBJECT
  for obj in response.localized_object_annotations:
    create_row(
      lista=rows, 
      fileID=fileID, 
      classe=obj.name, 
      percent=obj.score, 
      subclass='object'
    )
  # ITENS
  for label in response.label_annotations:
    create_row(
      lista=rows, 
      fileID=fileID, 
      classe=label.description, 
      percent=label.score, 
      subclass='item'
    ) 
  # FACE
  for _, face in enumerate(response.face_annotations, 1):
    face = {
      "Joy": face.joy_likelihood.name,
      "Exposed": face.under_exposed_likelihood.name,
      "Blurred": face.blurred_likelihood.name,
      "Rage": face.anger_likelihood.name,
      "Sad": face.sorrow_likelihood.name,
      "Hat": face.headwear_likelihood.name
    }
    for key in face.keys():
      if face[key] != 'VERY_UNLIKELY':
        create_row(
          lista=rows, 
          fileID=fileID, 
          classe=key, 
          percent=1, 
          subclass='face'
        )
  # TEXT
  try:
    create_row(
      lista=rows,
      fileID=fileID,
      classe=response.text_annotations[0].description.replace('\n', '_'),
      percent=1,
      subclass='text',
    )
  except:
    with open('erros.txt', 'a') as obj:
      obj.write(f'{response.text_annotations}, {fileID}\n')
  
  return rows

def load_labels(path_image: str, fileID = None) -> pd.DataFrame:
  if fileID == None: fileID=path_image
  features = [
    vision.Feature.Type.OBJECT_LOCALIZATION,
    vision.Feature.Type.FACE_DETECTION,
    vision.Feature.Type.LANDMARK_DETECTION,
    vision.Feature.Type.LOGO_DETECTION,
    vision.Feature.Type.LABEL_DETECTION,
    vision.Feature.Type.TEXT_DETECTION,
    vision.Feature.Type.DOCUMENT_TEXT_DETECTION,
    vision.Feature.Type.SAFE_SEARCH_DETECTION,
    vision.Feature.Type.IMAGE_PROPERTIES,
    vision.Feature.Type.CROP_HINTS,
    vision.Feature.Type.WEB_DETECTION,
    vision.Feature.Type.PRODUCT_SEARCH,
    vision.Feature.Type.OBJECT_LOCALIZATION,
  ]
  response = analyze_image_from_uri(path_image, features)
  return pd.DataFrame(rows_data(response, fileID))