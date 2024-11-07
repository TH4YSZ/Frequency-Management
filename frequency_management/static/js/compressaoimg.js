const sharp = require('sharp')
const fs = require('fs')

const imagens = fs.readdirSync('img')

imagens.forEach((imagem) => {
    if(imagem.endsWith(".jpg")){
        compressionImagem(imagem)
    }
})

async function compressionImagem(imagem){
    sharp(`img/${imagem}`)
    .jpeg({quality: 50})
    .resize(2000)
    .toFile(`teste/${imagem}`)
}