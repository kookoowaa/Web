# Django 웹 프레임워크

## Django에서의 어플리케이션 개발 방식

- 웹을 개발할 때 가장 먼저 해야 할 일은 프로그램이 해야 할 일을 적당한 크기로 나누어서 **모듈화 하는 것**
- 이 때 전체 프로그램 또는 모듈화된 단위 프로그램을 어플리케이션이라고 함
- Django에서는 전체 프로그램을 **프로젝트<sup>Project</sup>**, 모듈화된 단위 프로그램을 **어플리케이션<sup>Application</sup>**으로 명명
- 또 하나 알아둘 것은 **MVC<sup>Model-View-Controller</sup>**패턴으로 데이터<sup>Model, </sup>사용자 인터페이스<sup>View</sup>, 데이터를 처리하는 로직<sup>Controller</sup>을 구분해서 한 요소가 다른 요소들에 영향을 주지 않도록 설계하는 방식
- Django에서는 동일한 개념을 MVT<sup>Model-View-Template</sup>로 명명하며, 템플렛<sup>Template</sup>은 사용자에게 보여지는 UI 부분을, 뷰<sup>View</sup>는 실질적으로 프로그램 로직이 동작하고 결과를 템플릿에 전달하는 역할을 수행
- 