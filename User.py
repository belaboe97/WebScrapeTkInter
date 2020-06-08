class User():
    def __init__(self,username,gender,email,password,student,registerDate):
        self.__username=username
        self.__gender=gender
        self.__email=email
        self.__password=password
        self.__student = student
        self.__registerDate = registerDate

    def getUserName(self):
        return self.__username

    def getGender(self):
        return self.__gender

    def getEmail(self):
        return self.__email

    def getPassword(self):
        return self.__password

    def getStudent(self):
        return self.__student

    def getRegisterDate(self):
        return self.__registerDate

    def __str__(self):
        return self.__username + " with email: " + self.__email
