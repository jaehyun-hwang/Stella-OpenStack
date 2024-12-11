===============================
ku.stella
===============================

스텔라 클라우드 프로젝트

이 페이지는 Stella-OpenStack 코드 저장소입니다.

Stella-OpenStack은 OpenStack IaaS 클라우드에서 성능 SLA를 설정하기 위한 Stella VM 스케줄러를 지원합니다.

Stella 프로젝트에 대한 자세한 내용은 프로젝트 페이지를 방문하세요.

* 문서
        https://stella.korea.ac.kr
* 소스
        OpenStack 저장소: https://git.openstack.org/cgit/openstack/ku.stella

        GitHub 저장소: https://github.com/KUoslab/Stella-OpenStack
* 버그 신고
        이메일: starlab@os.korea.ac.kr

        Launchpad: https://bugs.launchpad.net/KU.stella

--------

* Stella-OpenStack API

Stella-OpenStack API(일명 Stella API)는 Stella-OpenStack 기능에 대한 접근을 제공합니다.

Stella API는 REST API(HTTP 기반 API)를 지원합니다.

Stella API 목록은 아래와 같습니다.

1. **/stella:**
        Stella 스케줄러(xGoS)와 Stella-OpenStack의 상태를 확인합니다.
2. **/stella/vms:**
        VM 목록과 각 VM의 정보를 반환합니다.
3. **/stella/vms/sla:**
        VM의 SLA를 설정합니다. Horizon에서 인스턴스 이름을 입력으로 사용합니다.
4. **/stella/hypervisor:**
        하이퍼바이저 호스트의 IP 주소를 반환합니다.

        'hypervisor_name' 필드는 필수입니다.
