### 파일 설명
- scapy_.py: 루트에서 visualizer로 가는 wisun(tab-windows로 생성하고, netsh로 바꾼 이름)인터페이스로 지나다니는 패킷을 캡처
    - 파일이름 처럼 scapy라는 패키지 활용
    - prn: 캡처한 패킷 핸들러 함수
    - count: 설정된 횟수만큼만 캡처(0이면 계속)
- socket_.py: ipv6-udp 소켓을 열어서 host로 보냄
    - AF_INET6: ipv6 사용을 설정
    - SOCK_DGRAM: udp 사용을 설정
- firestore_.py: observer에서 노드의 상태를 firestore에 저장 & firestore의 업데이트를 감지
    - set: 데이터를 저장
    - on_snapshot: 참조하고 있는 문서의 상태변화를 탐지
    - 지금은 그냥 테스트로 while true로 무한루프 돌려놓음(나중엔 다르게 하겠지)

- test.py: 그냥 내가 간단하게 테스트 하는파일
    - 이미 깃에 올려서 그냥 있음

### observer
- 역할
    1. visualizer가 있는 AP에서 실행되면서 wi-sun 모듈들의 상태를 관찰, 현재 상태를 서버(firebase)에 저장
    2. 서버에서 오는 요청을 노드로 전달
- 코드
    - firestore 객체에 eventListener를 등록해 document의 변화를 감지
        - 사용자 어플리케이션에서 모듈에 명령을 내릴때, 해당 모듈의 document의 필드값을 변경 함으로써 모듈과 통신
    - 'wisun' 인터페이스의 패킷을 관찰함으로써, 모듈의 상태를 파악
        - icmpv6.type.RPL_Control && icmpv6.code.Destination_Advertisement_Object_Acknowlegement 인 패킷을 찾으면 새로운 모듈이 네트워크에 등록되는 것을 감지
            - firestore에 새 모듈용 document를 생성
            - 'packetLoadToHex'함수를 만들어 load를 hex로 변환해, 새로운 모듈에 할당된 ip주소를 획득
        -  payload에 'check_reception'을 찾으면 해당 모듈에 차량의 현재 존재여부를 파악
            - 모듈에 해당하는 document를 업데이트(앱에서 확인가능)
    - soket을 활용하여 'wisun' 인터페이스로 패킷(명령)을 전송
        - 해당 모듈의 ip를 타겟으로 소켓을 열어 차단봉 통제에 관한 명령을 전달

- [참조](https://cloud.google.com/python/docs/reference/firestore/latest/google.cloud.firestore_v1.base_document.DocumentSnapshot)

### 중간보고서 내용
- 요구조건 및 제약 사항 분석에 대한 수정사항
- 설계 상세화 및 변경 내역
    - 구조도 그림 넣기
- 갱신된 과제 추진 계획
- 구성원별 진척도
- 보고 시점까지의 과제 수행 내용 및 중간 결과
