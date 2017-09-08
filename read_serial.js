const serialport = require('serialport')
const Readline = serialport.parsers.Readline

let portName = null
serialport.list(function(err, ports) {
    if (err) {
        console.log(err)
    }

    ports.forEach(function(port) {
        if (port.manufacturer == 'OpenMV') {
            portName = port.comName
        }
    })
    if (portName) {
        console.log('portName: ' + portName)
        open()
    } else {
        console.log('USB接続が確認できません')
    }
})

function open() {

    // require('serialport')がそのままコンストラクタ
    let port = new serialport(portName, {
        baudrate: 9600
    }, (err) => {
        if (err) {
            console.log(err)
        }
    })

    // parser
    const parser = port.pipe(new Readline({
        delimiter: '\n' // \r\n
    }))

    // 受信
    port.on('open', (err) => {
        if (err) {
            return console.log('Error opening port: ', err.message);
        }
        console.log('Serial open.')
        port.on('data', function(data) {
            let obj = spliter(data)
            if (obj) {
                // console.log(obj)
                if (obj.type == 'ping') {
                    pingProcess(port, obj.data)
                }
                if (obj.type == 'position') {
                    positionProcess(obj.data)
                }
            }
        })
    })

    port.on('error', (err) => {
        if (err) {
            console.log(err)
        }
    })

    port.on('close', () => {
        console.log('close')
    })

}

let pingTimeout = 3500
let lastPingTime = -1
let pingProcess = (port, data) => {
    lastPingTime = Date.now()
    if (data.fps) {
        console.log('fps: ' + Number(data.fps).toFixed(3))
    }
    setTimeout(() => {
        // console.log('ping  ' + (Date.now() - lastPingTime))
        if (Date.now() - lastPingTime >= pingTimeout) {
            port.close()
            open()
        }
    }, pingTimeout + 10)
}

let positionProcess = (data) => {
    let range = 0.20
    let target = {
        x: 0,
        y: 0,
        z: -5
    }
    let print = ''
    let Tx = Number(data.Tx) || 0
    let Ty = Number(data.Ty) || 0
    let Tz = Number(data.Tz) || 0
    Tx = Tx - target.x
    Ty = Ty - target.y
    Tz = Tz - target.z

    if (Tx < -range) {
        print += '← ' + Math.abs(Tx).toFixed(2) + ' '
    } else if (Tx > range) {
        print += '→ ' + Tx.toFixed(2) + ' '
    } else {
        print += '○ ' + range.toFixed(2) + ' '
    }

    if (Ty < -range) {
        print += '↓ ' + Math.abs(Ty).toFixed(2) + ' '
    } else if (Ty > range) {
        print += '↑ ' + Ty.toFixed(2) + ' '
    } else {
        print += '○ ' + range.toFixed(2) + ' '
    }

    if (Tz < -range) {
        print += '奥 ' + Math.abs(Tz).toFixed(2)
    } else if (Tz > range) {
        print += '引 ' + Tz.toFixed(2)
    } else {
        print += '○ ' + range.toFixed(2)
    }
    console.log(print)

    // Tx: '-1.633060',
    // Ty: '-1.421123',
    // Tz: '-3.273448',
    // Rx: '148.568558',
    // Ry: '312.042951',
    // Rz: '-57.953353'
}

let bufferData = ''
let spliter = (data) => {
    let splitData = (bufferData + String(data)).split(',')
    let head = 0
    let foot = splitData.length - 1
    let header = splitData[head]
    let footer = splitData[foot]
    if (checkHeader(header) && checkFooter(footer)) {
        bufferData = ''
        let type = splitData[1].trim()
        let data = {}
        for (let i = 2; i < foot; i++) {
            let d = splitData[i].split(':')
            if (d.length == 2) {
                let key = d[0].trim()
                let value = d[1].trim()
                data[key] = value
            }
        }
        let obj = {
            type: type,
            data: data
        }
        return obj
    } else {
        bufferData += String(data)
    }
    return null
}

let checkHeader = (header) => {
    header = String(header).trim()
    return header == 'st'
}

let checkFooter = (footer) => {
    footer = String(footer).trim()
    return footer == 'ed'
}
