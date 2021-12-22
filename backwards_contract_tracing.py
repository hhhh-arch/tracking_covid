# a correct implementation of potential_contacts(person_a, person_b)
# do not delete this line!
from reference import potential_contacts
# patient
person_a = []
# record the visits that might be infected by the virus
person_a = []
result = []
# record visits that is not infected by the virus
person_b = []
persons = []
def backward_contact_trace_1(person_o, person_a):
    # TODO
    resulf = {} 
    persons = [x[0] for x in person_o]
    # erase the people who is not the patient and has twice record 
    persons = set(persons)    
    
    for person in persons:
        person_b = [x for x in person_o if x[0] == person]
        contact = potential_contacts(person_a, person_b)
            
        if contact[0] != set():
            contact_lst = list(contact[0]) 
            contact_min = contact_lst[0]
            for contact_tup in contact_lst: 
                if contact_tup[1:4] < contact_min[1:4]:
                    contact_min = contact_tup
            resulf[person] = contact_min
            
    return resulf
# citing the function from previous section 
def forward_contact_trace(visits, index, day_time, second_order=False):
    # record of person who is affected by the first patient 
    
    resulf = []
    # visits' information is valid
    visit_tmp = [x for x in visits if len(x) == 7] 
    
    # patient
    person_a = [x for x in visit_tmp if x[0] == index and
                day_time <= (x[2], x[5], x[6])]
    # potential contacts 
    person_o = [x for x in visit_tmp if x[0] != index and
                day_time <= (x[2], x[5], x[6])]
    # no patients' record 
    if not person_a:
        return []
    
    # get person who contact with person_a
    resulf_dict1 = backward_contact_trace_1(person_o, person_a)
    # patient and visits has no contact records 
    if not resulf_dict1:
        return []
    # records of names for person who contact with patient 
    resulf = [x for x in resulf_dict1] 
    
    # the foward contact trace for people who is affected by the second patient 
    if second_order and resulf_dict1:
        for key, value in resulf_dict1.items():
            # the contacts that has not be checked before
            person_c = [x for x in person_o if x[0] not in resulf]  
            # patients' record
            person_a = [x for x in person_o if x[0] == key and 
                        value[1:4] <= (x[2], x[5], x[6])] 
            # potential contacts
            person_d = [x for x in person_c 
                        if value[1:4] <= (x[2], x[5], x[6])]
            # when there is no records of potential contacts
            if not person_d:
                continue
            resulf_dict2 = backward_contact_trace_1(person_d, person_a)
            # get name the other person who contact with second_order
            if resulf_dict2:
                resulf += [x for x in resulf_dict2]
    # sort the name list
    resulf = sorted(resulf) 
    return resulf

def backward_contact_trace(visits, index, day_time, window):
    resulf = []
    if len(day_time) != 3:
        return []
    if index == '':
        return []
    
    
    visit_tmp = [x for x in visits 
                 if x[2:5] < (x[2], x[5], x[6]) and len(x) == 7] 
    
    # record the visits that might be infected by the virus
    person_a = [x for x in visit_tmp if x[0] == index 
                and day_time[0] >= x[2] >= day_time[0]- window + 1
                and x[2:5] <= day_time]
    # record visits that is not infected by the virus
    person_o = [x for x in visit_tmp if x[0] != index 
                and day_time[0] >= x[2] >= day_time[0] - window + 1
                and x[2:5] <= day_time]
    if not person_a:
        return []
    
    # get person who contact with person_a
    resulf_dict1 = backward_contact_trace_1(person_o, person_a)
    # there is no contacts 
    if not resulf_dict1:
        return []
    
    resulf = [x for x in resulf_dict1] 
    
    # get KEY the person who contact with person_a
    
    for key, value in resulf_dict1.items():
            #  potential contacts
            person_c = [x for x in visit_tmp 
                        if x[0] not in resulf and x[0] != index]  
            
            resulf += forward_contact_trace(person_c, key, value[1:4])
    
    resulf = sorted(resulf) 
    
    return resulf
