function setCookie(name, value) {
    let Days = 30;
    let exp = new Date();
    exp.setTime(exp.getTime() + Days * 24 * 60 * 60 * 1000);
    document.cookie = name + "=" + escape(value) + ";expires=" + exp.toGMTString();
}

//读取cookies
function getCookie(name) {
    let reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)");
    let arr = document.cookie.match(reg)
    if (arr) {
        return unescape(arr[2]);
    }
    return null;
}

//删除cookies
function deleteCookie(name) {
    let exp = new Date();
    exp.setTime(exp.getTime() - 1);
    let cval = getCookie(name);
    if (cval != null) {
        document.cookie = name + "=" + cval + ";expires=" + exp.toGMTString();
    }
}

function getUser() {
    let user = getCookie('userid');
    if (user) {
        return user;
    }
    user = Math.floor(Math.random() * 1e8) ^ new Date().getTime();
    setCookie('userid', user);
    return user;
}


function parseQuery() {
    let pairs = location.search.substr(1).split('&')
    let ma = {}
    for (let i of pairs) {
        let res = i.split('=')
        if (res.length === 2) {
            const [k, v] = res
            ma[k] = v
        } else {
            ma[res[0]] = true
        }
    }
    return ma;
}

const roles = [
    { name: 'wolf', chinese: '狼', min: 1, max: 6, default: 3 },
    { name: 'civilian', chinese: '平民', min: 1, max: 6, default: 3 },
    { name: 'predictor', chinese: '预言家', min: 1, max: 1, default: 1 },
    { name: 'witch', chinese: '女巫', min: 1, max: 1, default: 1 },
    { name: 'hunter', chinese: '猎人', min: 1, max: 1, default: 1 },
    { name: 'guard', chinese: '守卫', min: 1, max: 1, default: 1 },
    { name: 'wolfKing', chinese: '白狼王', min: 1, max: 1, default: 0 },
    { name: 'wolfQueen', chinese: '狼美人', min: 1, max: 1, default: 0 },
    { name: 'qiubite', chinese: '丘比特', min: 1, max: 1, default: 0 },
    { name: 'wildChild', chinese: '野孩子', min: 1, max: 1, default: 0 },
    { name: 'idiot', chinese: '白痴', min: 1, max: 1, default: 0 },
]
const roleMap = {}
for (let i of roles) {
    roleMap[i.name] = i;
}