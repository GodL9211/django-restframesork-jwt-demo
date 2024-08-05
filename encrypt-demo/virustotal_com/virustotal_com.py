#! -*-conding: UTF-8 -*-
# @公众号: 海哥python

# https://www.virustotal.com/gui/home/upload


import execjs

js = """
function computeAntiAbuseHeader() {
    const e = Date.now() / 1e3;
    return btoa(`${(()=>{
        const e = 1e10 * (1 + Math.random() % 5e4);
        return e < 50 ? "-1" : e.toFixed(0)
    }
    )()}-ZG9udCBiZSBldmls-${e}`)
}
"""

if __name__ == '__main__':
    X_VT_Anti_Abuse_Header = execjs.compile(js).call('computeAntiAbuseHeader')
    print(X_VT_Anti_Abuse_Header)
