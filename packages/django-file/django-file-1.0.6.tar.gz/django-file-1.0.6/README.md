# django-file
Django File Relative

## Installation
```shell
pip install django-file
```

## Usage
```python
from django_file import calculate_md5

def xxx(request):
    photo = request.FILES.get('photo', '')
    # if photo:
    #     md5 = calculate_md5(photo)
    md5 = calculate_md5(photo)
```
