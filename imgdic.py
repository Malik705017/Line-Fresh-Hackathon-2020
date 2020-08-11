import random
def returnCard():
    imgDic = [
    "https://1.bp.blogspot.com/-tjlhN8T1tuM/Xy-3GnXSZzI/AAAAAAAACJA/DPCRvka3jHEyd3hb761TKBBqPdsjTu1pQCLcBGAsYHQ/s320/1.jpg",
    "https://1.bp.blogspot.com/-BGgFlm-0aB8/Xy-3J2F0vnI/AAAAAAAACJo/zyoYwqv3_wc3PPqAXwTd9IXztxYJt56DwCLcBGAsYHQ/s320/2.jpg",
    "https://1.bp.blogspot.com/-4AuiyUHwLnU/Xy-3Nef2UoI/AAAAAAAACKU/VE0SjTO_WSwmg5u4DG_bIhRNwXviNAKWQCLcBGAsYHQ/s320/3.jpg",
    "https://1.bp.blogspot.com/-q6FcamKMlko/Xy-3N0vr11I/AAAAAAAACKc/DBGxlajabc0Oqqc4zSpeWDMwZ497zozQwCLcBGAsYHQ/s320/4.jpg",
    "https://1.bp.blogspot.com/-m0f8Oo4d0Ak/Xy-3OFDtsPI/AAAAAAAACKg/dB2yfvVzRhM3tg76x5-SpvHo4NbluQfwwCLcBGAsYHQ/s320/5.jpg",
    "https://1.bp.blogspot.com/-TA1qNXl6JE0/Xy-3OZsR8FI/AAAAAAAACKk/lQFgbNWH--AaYzc03UlALSz_d1KcLyoDwCLcBGAsYHQ/s320/6.jpg",
    "https://1.bp.blogspot.com/-ryQ1IGgMV1g/Xy-3Os8pG-I/AAAAAAAACKo/TCZGtCaT68ALJm2WWtRtpcnxT3qxPBO8QCLcBGAsYHQ/s320/7.jpg",
    "https://1.bp.blogspot.com/-knBTmLTqn5c/Xy-3PESHUmI/AAAAAAAACKs/LuUICfU0BFALIaT7rjF5Qe4LahV-KuAWACLcBGAsYHQ/s320/8.jpg",
    "https://1.bp.blogspot.com/-uBtJ8vB6yyI/Xy-3PQWRa8I/AAAAAAAACKw/g6Wejxp_YpcE7F1SHxztxgNkEnqNMUFQACLcBGAsYHQ/s320/9.jpg",
    "https://1.bp.blogspot.com/-8S897R3XqsY/Xy-3GSAD13I/AAAAAAAACI8/IhZoqFcH00cKjeVrt1SJk-YEibBxGi1BQCLcBGAsYHQ/s320/10.jpg",
    "https://1.bp.blogspot.com/-rueLTFNO-_E/Xy-3GnR46_I/AAAAAAAACJE/rRbY3QfkxcMGYCxB9jTGt4LceUoog7QbgCLcBGAsYHQ/s320/11.jpg",
    "https://1.bp.blogspot.com/-OgHmaVu2OfM/Xy-3HTTZuaI/AAAAAAAACJI/NvKjSj8QUFU2wOTuvAXpNtO2SWIDzXONgCLcBGAsYHQ/s320/12.jpg",
    "https://1.bp.blogspot.com/-tclqh8avd2g/Xy-3HlDSioI/AAAAAAAACJM/Qq76X7CxPb8qtllKrwwGd2DB2Oqq-ElKgCLcBGAsYHQ/s320/13.jpg",
    "https://1.bp.blogspot.com/-21Qll81dlVo/Xy-3H9xQPYI/AAAAAAAACJQ/Ay-paDsf-osnaJ-a2ul6vg6iwiSaL9KawCLcBGAsYHQ/s320/14.jpg",
    "https://1.bp.blogspot.com/-tMWlTYOdf7k/Xy-3IF1FbHI/AAAAAAAACJU/cKBQ_qn2y_seA6BjRsKCvE9v-7LSKiHMQCLcBGAsYHQ/s320/15.jpg",
    "https://1.bp.blogspot.com/-QFgWf7zlBQI/Xy-3IqDWs5I/AAAAAAAACJY/vO37lO5q-lIO8kmpieCFOALH1p5j57g-gCLcBGAsYHQ/s320/16.jpg",
    "https://1.bp.blogspot.com/-UhBzwFMOt6E/Xy-3I4YJFOI/AAAAAAAACJc/f6acSQQhlekirbEDjHlI1BXFPlttkc9XQCLcBGAsYHQ/s320/17.jpg",
    "https://1.bp.blogspot.com/-Kuo8eJalFCc/Xy-3JL9n72I/AAAAAAAACJg/NIoWxYKjIrgB7CeKEjFg3zlo83rOG3HHgCLcBGAsYHQ/s320/18.jpg",
    "https://1.bp.blogspot.com/-J5hcR13mMo0/Xy-3JWq7YRI/AAAAAAAACJk/WQSYDrEdo4wj_-HBigUpsUc8dsTeXZ3yQCLcBGAsYHQ/s320/19.jpg",
    "https://1.bp.blogspot.com/-ousrGTlg5NA/Xy-3JzVqMpI/AAAAAAAACJs/ncTfM-T1nzAkQu7S-OaZmGFumCJKtxEgQCLcBGAsYHQ/s320/20.jpg",
    "https://1.bp.blogspot.com/-eGdOOGWSIig/Xy-3KTqjQPI/AAAAAAAACJw/vhmHeKOT4oQUMXz-fe0sOX9Ldmbk3josACLcBGAsYHQ/s320/21.jpg",
    "https://1.bp.blogspot.com/-2AO66nUvGcU/Xy-3KhnS42I/AAAAAAAACJ0/ceYwkUcc_hsBi2LSrqIQo5wiXhPRzIR3wCLcBGAsYHQ/s320/22.jpg",
    "https://1.bp.blogspot.com/-2AO66nUvGcU/Xy-3KhnS42I/AAAAAAAACJ0/ceYwkUcc_hsBi2LSrqIQo5wiXhPRzIR3wCLcBGAsYHQ/s320/22.jpg",
    "https://1.bp.blogspot.com/-2AO66nUvGcU/Xy-3KhnS42I/AAAAAAAACJ0/ceYwkUcc_hsBi2LSrqIQo5wiXhPRzIR3wCLcBGAsYHQ/s320/22.jpg",
    "https://1.bp.blogspot.com/-38ALZ4RmYdo/Xy-3K1wEg6I/AAAAAAAACJ4/3H4sX01iPzc9sityWYwnczFjfREL8ZNIACLcBGAsYHQ/s320/23.jpg",
    "https://1.bp.blogspot.com/-38ALZ4RmYdo/Xy-3K1wEg6I/AAAAAAAACJ4/3H4sX01iPzc9sityWYwnczFjfREL8ZNIACLcBGAsYHQ/s320/23.jpg",
    "https://1.bp.blogspot.com/-38ALZ4RmYdo/Xy-3K1wEg6I/AAAAAAAACJ4/3H4sX01iPzc9sityWYwnczFjfREL8ZNIACLcBGAsYHQ/s320/23.jpg",
    "https://1.bp.blogspot.com/-F-TcnWZydJY/Xy-3LJkneaI/AAAAAAAACJ8/qf67BCHq9gsK7KNqjLUwDCozCZCjzlDfQCLcBGAsYHQ/s320/24.jpg",
    "https://1.bp.blogspot.com/-F-TcnWZydJY/Xy-3LJkneaI/AAAAAAAACJ8/qf67BCHq9gsK7KNqjLUwDCozCZCjzlDfQCLcBGAsYHQ/s320/24.jpg",
    "https://1.bp.blogspot.com/-F-TcnWZydJY/Xy-3LJkneaI/AAAAAAAACJ8/qf67BCHq9gsK7KNqjLUwDCozCZCjzlDfQCLcBGAsYHQ/s320/24.jpg"
    ]

    randNum = random.randint(0,29)

    url = imgDic[randNum]
    return(url)

datacount = 0