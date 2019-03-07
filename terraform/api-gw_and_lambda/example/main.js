<<<<<<< HEAD
version https://git-lfs.github.com/spec/v1
oid sha256:2de9da87bb6ceac7dcc7359638152e598711d624bfa7ce42835260b7f934e719
size 263
=======
'use strict'

exports.handler = function(event, context, callback) {
  var response = {
    statusCode: 200
    headers: {
      'Content-Type': 'text/html; charset=utf-8'
    },
    body: '<p>Hello World!</p>'
  }
  callback(null, response)
}
>>>>>>> e9ce1554c7cb8ee68498265c8f28104c05af85a3
