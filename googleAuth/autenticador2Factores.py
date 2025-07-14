import pyotp
import qrcode
class Autenticador2FA:
    def generarClaveSecreta(self):
        return pyotp.random_base32()
        #return "FQW4YWWJEO3XNEHVOV33RUAC376N4OIO"
    
    def generarURI(self,claveSecreta, usuario, nombreAplicacion):
        totp=pyotp.TOTP(claveSecreta)
        uri=totp.provisioning_uri(name=usuario, issuer_name=nombreAplicacion)
        return uri
    
    def generarCodigoQR(self, uri, usuario):
        qr_img=qrcode.make(uri)
        qr_img.save(f"qr_{usuario}.png")
        return f"qr_{usuario}.png"
    
    def verificarCodigo(self, codigo,claveSecreta):
        totp=pyotp.TOTP(claveSecreta)
        return totp.verify(codigo)
    