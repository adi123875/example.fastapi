from fastapi import APIRouter,Depends,status,HTTPException,Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import session
from ..database import get_db
from ..import models,schemas,utils,oauth2
router=APIRouter(tags=['authentication'])

@router.post("/login",response_model=schemas.token)
async def login(user_crendentials:OAuth2PasswordRequestForm=Depends(),db:session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.email==user_crendentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"invaild crendentials")
    if not utils.verify(user_crendentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"invaild password")
    access_token=oauth2.create_access(data={"user_id":user.id})
                                            
                                            
    return {"access_token":access_token,"token_type":"bearer"}