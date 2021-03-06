import requests
import json
import math


class RateMyProfScraper:
    def __init__(self, schoolid):
        self.UniversityId = schoolid
        self.professorlist = self.createprofessorlist()
        self.indexnumber = False

    # creates List object that include basic information on all Professors from the IDed University
    def createprofessorlist(self):
        tempprofessorlist = []
        num_of_prof = self.GetNumOfProfessors(self.UniversityId)
        num_of_pages = math.ceil(num_of_prof / 20)
        i = 1
        while (i <= num_of_pages):  # the loop insert all professor into list
            page = requests.get("http://www.ratemyprofessors.com/filter/professor/?&page=" + str(
                i) + "&filter=teacherlastname_sort_s+asc&query=*%3A*&queryoption=TEACHER&queryBy=schoolId&sid=" + str(
                self.UniversityId))
            temp_jsonpage = json.loads(page.content)
            temp_list = temp_jsonpage['professors']
            tempprofessorlist.extend(temp_list)
            i += 1
        return tempprofessorlist

    # function returns the number of professors in the university of the given ID.
    def GetNumOfProfessors(self, id):
        page = requests.get(
            "http://www.ratemyprofessors.com/filter/professor/?&page=1&filter=teacherlastname_sort_s+asc&query=*%3A*&queryoption=TEACHER&queryBy=schoolId&sid=" + str(
                id))  # get request for page
        temp_jsonpage = json.loads(page.content)
        num_of_prof = temp_jsonpage[
            'remaining'] + 20  # get the number of professors
        return num_of_prof

    def SearchProfessor(self, ProfessorName):
        index = self.GetProfessorIndex(ProfessorName)
        if (index):
            self.indexnumber = index - 1
            return True
        return False

    # function searches for professor in list
    def GetProfessorIndex(self, ProfessorName):
        for i in range(0, len(self.professorlist)):
            if (ProfessorName == (self.professorlist[i]['tFname'] + " " + self.professorlist[i]['tLname'])):
                return i + 1
        return False  # Return False is not found

    def PrintProfessorInfo(self):  # print search professor's name and RMP score
        if self.indexnumber == False:
            print("error")
        else:
            print(self.professorlist[self.indexnumber])

    # print search professor's name and RMP score
    def getProfessorDetail(self, key):
        if self.indexnumber == False:
            return ''
        else:
            return self.professorlist[self.indexnumber][key]
