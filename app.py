from flask import Flask, escape, request
import filetodb

app = Flask(__name__)
fd = filetodb.Filetodb()


@app.route('/')
def hello():
    name = request.args.get("name", "Crot")
    return f'Hello, {escape(name)}!'

@app.route('/insert/<filename>')
def storedata(filename):
    #token = request.form['token']
    df = fd.openFile(filename)
    df = fd.cleanEmptyCell(df)
    df = fd.checkSetHeader(df,'upload_id')
    df = fd.joinDatetime(df,'expired_date','expired_time')
    
    df = fd.fixEmail(df,'customer_email')
    df = fd.cekEmailValid(df, 'customer_email')
    df = fd.fixPhoneNumber(df,'customer_phone')
    
    invalidemails = fd.getInvalidEmails(df,'customer_email')
    unregisteredemail = fd.getUnregEmails()
    unregisteredphone = fd.getUnregPhones()
    
    if len(invalidemails) == 0 and len(unregisteredemail) == 0 and len(unregisteredphone) == 0:
        fd.toDB(df)
        results='ok'
    else:
       results='{ "invalid_phones" :'
       results=results+unregisteredphone
       results=results+','
       results=results+' "invalid_emails" :'
       results=results+unregisteredemail
       results=results+'}'
       
    return results
