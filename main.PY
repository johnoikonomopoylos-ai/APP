from fastapi import FastAPI, Depends, HTTPException, status
from mysql import engine, Base, get_db
from sqlalchemy.orm import Session
from model import User
from typing import List

#BIBLIOTHIKES POY XREIAZONTAI GIA HTTP BASIC AUTH
import secrets
from fastapi.security import HTTPBasic,HTTPBasicCredentials
from passlib.context import CryptContext

#EISAGOGH BIBLIOTHIKHS GIA PROSTASIA APO KAKOBOYLA
#JAVASCRIPT REQUEST-PAROXH MEGALYTERHS ASFALEIAS
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

#ΕΝΤOLES PROS TO BACKEND NA STEILEI EIDIKES ADEIES STON BROWSER
#OPVS ANAGNVSH APO SYGKEKRIMENH DIEYUYNSH FRONTEND K.A. TYPOS
#ENTOLVN POY MPOREI NA STEILEI TO FRONTEND K.O.K.EPITREPOYN STO 
#BACKEND NA EPIKOINVNΕI ME TO FRONTEND
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","http://localhost:5173"],  # Για τοπική ανάπτυξη. Στην παραγωγή βάλε το ακριβές URL του frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)

#O KYRIOS ALGORITHMOS POY THA XRHSIMOPOIHUEI KAI APOTROPH EISAGVGHS PALIOTERVN ALGOIUMVN
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#DHMIOYRGIA ASFALOYS LOG IN ME METHODO HTTP BASIC AUTHRIZATION
security=HTTPBasic()

#DHMIOYRGIA SYNARTHSHS POY UA EKTELEITAI KAUE FORA POY KAPOIOS XRHSTHS
#PROSPATHEI NA MPEI SE PROSTATEYMENO ENDPOINT

def get_current_user(credentials: HTTPBasicCredentials = Depends(security),
    db: Session = Depends(get_db),):
    # 1. Αναζήτηση του χρήστη στη βάση δεδομένων με βάση το email
    user = db.query(User).filter(User.username == credentials.username).first()
    
    # 2. Έλεγχος αν ο χρήστης υπάρχει και αν το password είναι σωστό
    # Χρησιμοποιούμε secrets.compare_digest για προστασία από timing attacks
    if not user or not pwd_context.verify(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Λανθασμένο όνομα χρήστη ή κωδικός πρόσβασης",
            headers={"WWW-Authenticate": "Basic"},
        )
        
    return user

#PROSTATEYMENO ENDPOINT AUTHORISED_USER_DATA POY MAS EPISTREFEI TA DATA TOY DIAPISTEYMENOY XRHSTH

@app.get("/users/Authorized_data")
def read_current_user(current_user: User = Depends(get_current_user)):
    return {"username": current_user.username, "email": current_user.email}






@app.get ("/")
def home():
    return{'home':'hallo'}

@app.get("/sql")
def databasecreation(db : Session = Depends(get_db)):
    return{'message':"db created succesfully"}

@app.post("/create-user/{username}/{email}/{password}")
def create_user(username:str,email:str,password:str, db: Session = Depends(get_db)):
    hashed_password=pwd_context.hash(password) 
     #1. Δημιουργία του αντικειμένου/εγγραφής
    new_user = User(username=username,email=email,hashed_password=hashed_password)
    
    # 2. Εισαγωγή στη βάση δεδομένων (Προετοιμασία)
    db.add(new_user)
    
    # 3. Οριστικοποίηση της εγγραφής (Save/Commit)
    db.commit()
    
    # 4. (Προαιρετικό) Ανανέωση του αντικειμένου για να πάρετε το ID που δημιουργήθηκε αυτόματα
    db.refresh(new_user)

    
    return {"message": "Ο χρήστης δημιουργήθηκε!", "user_id":new_user.id}


#ENDPOINT POY EPISTREFEI OLA TA STOIXEIA THS BASHS DEDOMENVN

@app.get("/get_all_users")
def get_all_users(db: Session = Depends(get_db)):
    # Ανάκτηση όλων των εγγραφών από τον πίνακα user
    users = db.query(User).all()
    
    return users

#ENDPOINT POY DIAGRAFEI XRHSTH ME SYGKEKRIMANO ID
@app.delete("/delete_user/{id}")  # 1. Καλύτερη πρακτική να περνάει το id ως path parameter
def delete_user(id: str, db: Session = Depends(get_db)):
    # 2. Αναζήτηση του χρήστη στη βάση (χρησιμοποιούμε .first() για να πάρουμε το object)
    db_user = db.query(User).filter(User.id == id).first()
    
    #3. Έλεγχος αν ο χρήστης ΔΕΝ υπάρχει
    if db_user is None:
      return {"message": "Ο χρήστης δεν υπάρχει", "user_id":id}
                 
        
    # 4. Προετοιμασία και οριστικοποίηση της διαγραφής
    db.delete(db_user)
    db.commit()

   
    # 5. Επιστροφή επιτυχούς μηνύματος
    return  {"message": "Ο χρήστης διαγραφηκε", "user_id":id}
