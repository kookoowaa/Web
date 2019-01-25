# 포스트 기능(form)

`index.py`

```python
print('''
<!doctype html>
<html>
<head>
  <title>WEB1 - Welcome</title>
  <meta charset="utf-8">
</head>

<body>
  <h1><a href="index.py">WEB</a></h1>
  <ol>{list}</ol>
  <a href = "create.py">create</a>
  <h2>{title}</h2>
  <p>{desc}</p>


</body>

'''.format(title=pageId, desc = description, list = listStr))
```

`create.py`

```python
print('''
<!doctype html>
<html>
<head>
  <title>WEB1 - Welcome</title>
  <meta charset="utf-8">
</head>

<body>
  <h1><a href="index.py">WEB</a></h1>
  <ol>{list}</ol>
  <a href = "create.py">create</a>
  <form action='process_create.py' method="post">
    <p><input type ='text' name='title' placeholder='title'></p>
    <p><textarea rows = '4' name='description' placeholder='description'></textarea></p>
    <p><input type='submit'></p>
  </form>


</body>

'''.format(title=pageId, desc = description, list = listStr))
```

- 사용자가 정보를 남기는 과정은 어떻게 이루어질까?
  1. 먼저 기존의 `index.py`에 입력 기능을 담은 `create.py`로의 링크 생성
  2. `create.py`는 `index.py`와 상당히 유사한 html 형식을 다루며 `<p>`태그 안에 새로운 형식의 태그 생성 (input과 textarea)
  3. `<input>`태그에서 `type='text'`로 지정 시 글 작성이 가능한 박스가 생성됨
  4. `<input>`태그에서 `type='submit'`을 지정 시 입력 버틍이 생성됨
  5. `<textarea>` 태그는 글작성이 가능한 박스를 생성하며 위 `<input>`태그와는 다르게 위아래로 긴 글상자가 생성됨 (`rows='#'`를 인자로 입력받음)
  6. `<input>`과 `<textarea>` 공통으로 `placeholder`와 `name`을 인자로 입력 받음(선택)
  7. `placeholder`는 화면에 출력되는 문구로, 글상자가 비어 있을 때 인자로 입력받은 내용을 사용자에게 보여줌
  8. `name`은 사용자로부터 입력받은 내용을 전달 받을 때 query 값으로 사용됨 (i.e. `http://<ip address>/create.py?title=<입력값>?description=<입력값>`)
  9. 위 `<input>`과 `<textarea>`가 있는 `<p>` 태그를 **`<form>` 태그로 연결**
  10. `<form>` 태그는 `action = '<파일명>'`과 `method`를 인자로 받는데 `method`는 default 값으로 `method="GET"`을 지정
  11. 위의 경우 모든 query 과정이 url에 드러나게 되고 외부로부터 부적절하게 사용될 가능성이 다분
  12. `method="post"`로 지정 시 사용자의 데이터가 기록되는 과정이 url에 나타나지 않음