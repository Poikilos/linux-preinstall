# Document ETL

ETL stands for "extract transform and load" and is the process of automating document processing for the purpose of putting specific information from documents into databases.


## Word or Writer image extraction
(via unzip and emf conversion)
```
#!/bin/bash
# Neither of the websites provide a pixel perfect method.
# see also https://stackoverflow.com/questions/15063349/imagemagick-on-linux-to-convert-emf-to-png/28749719#28749719
# cited by https://askubuntu.com/questions/533665/convert-emf-to-png-image-using-command-line

suffix="_FILES"
folder_name="$1$suffix"
if [ -z "$1" ]; then
  echo "ERROR: nothing done since you must specify a docx file"
  exit 1
fi
if [ ! -d "$folder_name" ]; then
  if [ ! -f "$1" ]; then
    echo "ERROR: nothing done since $1 does not exist."
    exit 2
  fi
  unzip "$1"
fi
if [ ! -d "$folder_name" ]; then
  echo "ERROR: Nothing done since you must first extract $1 here to get $folder_name"
  exit 1
fi

ex_images_path="$folder_name/word/media"

echo "The code below is deprecated since it is not pixel perfect (is DPI based)"
echo "Instead, manually open "$ex_images_path/image*.emf files one by one in Inkscape, then in the program right-click the image that appears, then use 'Extract Image' feature."
exit 0


convert_emf()
{
  this_name="$1"
  source_path="$ex_images_path/$this_name.emf"
  dest_path="$this_name.png"
  #libreoffice --headless --convert-to png "$try_path"
  inkscape -e "$dest_path" --export-dpi=600 "$source_path"
}

try_convert_emf()
{
  this_name="$1"
  try_path="$ex_images_path/$this_name.emf"
  if [ -f "$try_path" ]; then
    echo "converting $this_name..."
    convert_emf "$this_name"
  else
    echo "no $try_path so quitting."
    exit 0
  fi
}

try_convert_emf "image1"
try_convert_emf "image2"
try_convert_emf "image3"
try_convert_emf "image4"
try_convert_emf "image5"
try_convert_emf "image6"
try_convert_emf "image7"
try_convert_emf "image8"
try_convert_emf "image9"
try_convert_emf "image10"
```
