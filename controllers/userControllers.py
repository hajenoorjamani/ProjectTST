from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from models.userModels import User, UserSchema, AnswerSchema
from fastapi import HTTPException, status
from auth.hash_password import HashPassword
from auth.jwt_handler import create_access_token
from pydantic import EmailStr
from random import choice, choices


def sign_up(request: UserSchema, db: Session):
    user = db.query(User).filter(User.email == request.email).first()

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email sudah digunakan."
        )

    if len(request.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Password setidaknya memiliki 8 karakter."
        )

    hashed_password = HashPassword().create_hash(request.password)
    new_user = User(email=request.email, nama=request.nama,
                    password=hashed_password, recommendation="")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "Pesan": "Akun berhasil dibuat."
    }


def sign_in(request, db: Session):
    user = db.query(User).filter(User.email == request.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Akun dengan email tersebut tidak ditemukan."
        )

    if not HashPassword().verify_hash(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Gagal, silahkan periksa email/password Anda kembali!")

    access_token = create_access_token(user.email)

    return {"access_token": access_token, "token_type": "bearer"}


def get_all_user(db: Session):
    return db.query(User).all()


def get_user(id: int, db: Session):
    user = db.query(User).filter(User.userID == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User dengan id tersebut tidak ditemukan."
        )

    return user

def findMovieRecommendation(request: AnswerSchema, db: Session, user: str):
    updateUser = db.query(User).filter(User.email == user)

    answers = [request.question_answer_1, request.question_answer_2, request.question_answer_3, request.question_answer_4, request.question_answer_5]
    
    totalSkor = 0
    genderSkor = 0
    randomSkor1 = 0 
    randomSkor2 = 0
    genreAnswer = choices(["'Romance'", "'Family'", "'Animation'", "'Action'", "'Horror'", "'Comedy'", "'Drama'", "'Fantasy'", "'Sci-fi'"])
    yearAnswer = choice([1990, 2000, 2010])

    if(answers[0] == 1):
        genderSkor = genderSkor + 2
    elif(answers[0] == 2):
        genderSkor = genderSkor + 3
    elif(answers[0] == 3):
        genderSkor = genderSkor + 5
    
    
    if(answers[1] == 1):
        genreAnswer = ["'Romance'", "'Family'", "'Animation'"]
    elif(answers[1] == 2):
        genreAnswer = ["'Action'", "'Horror'", "'Comedy'"]
    elif(answers[1] == 3):
        genreAnswer = ["'Drama'", "'Fantasy'", "'Sci-fi'"]

    if(answers[2] == 1):
        randomSkor1 = randomSkor1 + 2
    elif(answers[2] == 2):
        randomSkor1 = randomSkor1 + 3
    elif(answers[2] == 3):
        randomSkor1 = randomSkor1 + 5

    if(answers[3] == 1):
        randomSkor2 = randomSkor2 + 2
    elif(answers[3] == 2):
        randomSkor2 = randomSkor2 + 3
    elif(answers[3] == 3):
        randomSkor2 = randomSkor2 + 5
        
    if(answers[4] == 1):
        yearAnswer = 2000
    elif(answers[4] == 2):
        yearAnswer = 3000
    elif(answers[4] == 3):
        yearAnswer = 1990
    
    totalSkor = (randomSkor1 * randomSkor2) // genderSkor
    randomNumberGenre = totalSkor % 3
    genreRecommedation = genreAnswer[randomNumberGenre]

    # rekomendasi = db.execute("SELECT * FROM movies WHERE movieGenre='D")
    print("heuheuheuehueh")
    moviesRecommendation = db.execute("SELECT * FROM movies WHERE movieGenre=%s AND movieYear<%d" % (genreRecommedation, yearAnswer)).fetchall()
    for movie in moviesRecommendation:
        print(movie)
    randomNumberMovieRecommendation = ((randomSkor1 + randomSkor2)**genderSkor) % len(moviesRecommendation)
    # print(randomNumberMovieRecommendation)
    # print(((randomSkor1 + randomSkor2)**genderSkor))
    dataMovieRecommendation = moviesRecommendation[randomNumberMovieRecommendation]

    movieRecommendation = dataMovieRecommendation[1] + " (" + str(dataMovieRecommendation[2]) + ")"

    updateUser.update({'recommendation': movieRecommendation})
    db.commit()

    return {"movie recommendation": movieRecommendation}
