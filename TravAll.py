startingPoint = input('Enter Starting Point: ')
destinationPoint = input('Enter Destination point: ')

class TravelInstance:
    def __init__(self, starting, destination):
        self.start = starting
        self.dest = destination
        
    def GetFromGmapsAPI(self):
        #this is a function that mimis the google maps api. the train, bus, walking and private vehicle data would be obtained from various sources like Google maps, bmtc data and IRCTC data 
        # walking -> 0
        # bus -> 1
        # train -> 2
        # cab/auto -> 3
        # private vehicle(car) -> 4
        # private vehicle(bike) -> 5

        travelOptions = {1: [3,2,1,0,1.47, 95], 2: [0,1,2,3,1.40, 67], 3: [0,1,2,1,0,1.30, 27], 4: [3,1.00, 50], 5: [4,0.45, 70], 6: [5,0.37, 90]}
        #format <option number>: [<usage flow>, <total time(hrs.minutes)>, <total cost>]


        trains = []
        trains.append('')
        trains.append({2 : ['613485', 68, 73, '14:25', '14:40', 15, 45]})
        trains.append({3 : ['527105', 68, 73, '19:08', '19:22', 14, 50]})
        trains.append({3 : ['209312', 68, 73, '19:10', '19:25', 15, 40]})
        #format <point from>: [ <train 6 digit unique identification number>, <onboarding station code>, <deboarding station code> , <departure time>, <arrival time>, <travel time(minutes)>, <cost>]


        buses = []
        buses.append('')
        buses.append({3: ['114C','14:50',30,20]})
        buses.append({2: ['256B','18:40',15,15]})
        buses.append({2: ['144G', '18:30', 17,15], 4: ['115D', '19:30', 25, 20]})
        #format <point from>[<bus number>,  <departure time from relavent bust stop>, <travel time(minutes)>, <cost>]

        walking = []
        walking.append('')
        walking.append({4: 20})
        walking.append({1: 5})
        walking.append({1: 5, 5: 20})
        #format <point from>[ <travel time(minutes)>]

        privateCar = []
        for _ in range(5):
          privateCar.append('')
        privateCar.append({1: [20, 50]})
        #format <point from>[ <travel time(minutes)>, <cost>]
        #cost => fuel

        privateBike = []
        for _ in range(6):
          privateBike.append('')
        privateBike.append({1: [15, 45]})
        #format <point from>[ <travel time(minutes)>, <cost>]
        #cost => fuel
        
        self.trains = trains
        self.buses = buses
        self.travelOptions = travelOptions
        self.walking = walking
        self.privateCar = privateCar
        self.privateBike = privateBike


    def GetFromOlaAPI(self):
      # this function mimics the use of the Ola API. This could be easily extended to other cab services like Uber(Uber API). 
      taxiOla = []
      taxiOla.append('')
      taxiOla.append({1:[1, 2, 10, 95]})
      taxiOla.append({4: [2, 4, 45, 120]})
      taxiOla.append('')
      taxiOla.append({1: [1, 6, 24, 150]})
      # car(4 wheeler) -> 1
      # auto(3 wheeler) -> 2
      #format <point from>[<vehicle type>,  <time left for arrival(minutes)>, <travel time(minutes)>, <cost>]
      self.taxiOla = taxiOla
    
    #popDensity => Population density. It can be obtained from the actual Google maps api. 
    def GetBusRiderROI(self,busNumber, departure_time, popDensity):
      #in this function, we could use a trained machine learning predictor to predict the number of people getting on and getting off at the intermediate stops, which could then be used in meausuring ROI. 
      #the data used for training could be given to use by the various government transport bodies, like BMTC, KSRTC etc..
      return 4 #just returning a sample value for demonstration purpose.

    def GetTrainRiderInfo(self,TrainNumber, departure_time, popDensity):
      #in this function, we could use a trained machine learning predictor to predict the number of people getting on and getting off at the intermediate stops, which could then be used in meausuring ROI. 
      #the data used for training could be given to us by IRCTC. 
      return 4 #just returning a sample value for demonstration purpose. 
    
    def GetCabOrAutoROI(self,RegNumber):
      #the ROI for a cab/auto could be calculated using various parameters such as - if it has been regularly disinfected, if a person who was later known to have the disease used that vehicle etc..
      return 4 #just returning a sample value for demonstration purpose. 

    def GetWalkingROI(self,popDensity):
      #ROI is calculated based on flow of people(inferred from population density). 
      return 3 #just returning a sample value for demonstration purpose. 

    #ROI - Risk of Infection
    def GetROI(self):
      # walking -> 0
      # bus -> 1
      # train -> 2
      # cab/auto -> 3
      # private vehicle(car) -> 4
      # private vehicle(bike) -> 5
      avgROI = []
      for i in range(1,7):
        k = 1
        ROI = 0
        for j in self.travelOptions[i][:-2]:
          if j == 0: 
            ROI = ROI + self.GetWalkingROI(10)
          elif j == 1:
            ROI = ROI + self.GetBusRiderROI(self.buses[i][k][0], self.buses[i][k][1], 10) #10 is just a sample population density for demnstration purpose. We would actually be getting it from the Google Maps API.
            print(self.buses[i][k])
          elif j == 2:
            ROI = ROI + self.GetTrainRiderInfo(self.trains[i][k][0], self.trains[i][k][3], 10) #10 is just a sample population density for demnstration purpose. We would actually be getting it from the Google Maps API.
          elif j == 3:
            ROI = ROI + self.GetCabOrAutoROI(4037) # This is just a sample registration number of the vehicle. We would actually be getting it from the Ola/Uber API. 
          elif j == 4:
            ROI = ROI + 0 
          elif j == 5:
            ROI = ROI + 0
          k = k + 1
        
        avg = ROI/(k-1)
        avgROI.append(avg)
        self.avgROI = avgROI
      return avgROI

    def RankRecs(self, ROI_list):
      #in this function, we implement the optimization function, where we find the best recommendations to give to the user given the cost, ROI, estimated time taken for travel and the user's past preferences.
      new_list = []
      for i in range(1,7):
        new_list.append(ROI_list[i-1]+self.travelOptions[i][-2]+self.travelOptions[i][-1]) #most basic form of optimization function where all the weights is equal to 1. 
      dict = {}
      for i in range(1,7):
        dict[i] = new_list[i-1]
      #print(dict)
      self.dict = dict
      sorted_keys = sorted(dict, key=dict.get)
      return sorted_keys
      
    def displayTravelOptions(self, TravelRank):
      for i in range(1,7):
        print(i, ' ',startingPoint, ' -> ', end='')
        for j in self.travelOptions[TravelRank[i-1]][:-2]:
          if j == 0:
            print('Walking -> ', end='')
          elif j == 1:
            print('Bus -> ', end='')
          elif j == 2:
            print('Train -> ', end='')
          elif j == 3:
            print('Cab/auto -> ', end='')
          elif j == 4:
            print('Private Vehicle(Car) -> ', end='') 
          elif j == 5:
            print('Private Vehicle(Bike) -> ', end='')
        print(destinationPoint)
        print('ROI = ', self.avgROI[TravelRank[i-1] - 1])
        print('cost = ', self.travelOptions[TravelRank[i-1]][-1])
        print('time for travel = ', self.travelOptions[TravelRank[i-1]][-2], ' hours')
        print('')

    def ShowSummary(self,option, TravelRank):
      print(startingPoint, ' -> ')
      k = 1
      for j in self.travelOptions[TravelRank[option-1]][:-2]:
        if j == 0:
          print(k)
          print('Walking -> ')
          print('for ', self.walking[TravelRank[option - 1]][k], 'minutes')
        elif j == 1:
          print(k)
          print('Bus -> ')
          print('number ', self.buses[TravelRank[option-1]][k][0], 'at ', self.buses[TravelRank[option-1]][k][1])
        elif j == 2:
          print(k)
          print('Train -> ')
          print('number ', self.trains[TravelRank[option-1]][k][0], 'at station ', self.trains[TravelRank[option-1]][k][1], ' and alight at ', self.trains[TravelRank[option-1]][k][2], ' onboard at time ', self.trains[TravelRank[option-1]][k][3], ' and alight at time ', self.trains[TravelRank[option-1]][k][4])
        elif j == 3:
          print(k)
          print('Cab/auto -> ')
          print('will arrive in', self.taxiOla[TravelRank[option - 1]][k][1], ' minutes')
        elif j == 4:
          print(k)
          print('Private Vehicle(Car) -> ') 
          print('Time to travel: ', self.privateCar[TravelRank[option-1]][k][0], ' minutes')
        elif j == 5:
          print('Private Vehicle(Bike) -> ')
          print('Time to travel: ', self.privateBike[TravelRank[option - 1]][k][0], ' minutes')
        k = k + 1
      print(destinationPoint)
      print('')


inst = TravelInstance(startingPoint, destinationPoint)
TravelInstance.GetFromGmapsAPI(inst)
TravelInstance.GetFromOlaAPI(inst)
ROI_list = TravelInstance.GetROI(inst)
TravelRank = TravelInstance.RankRecs(inst, ROI_list)

lt = [1,2,3,4,5,6]
print('before sorting based on cost, latency and Risk Of infection')
TravelInstance.displayTravelOptions(inst, lt)
print('after')
print('******************************************************************************************')
TravelInstance.displayTravelOptions(inst, TravelRank)


option = int(input('Select your travel flow choice: '))
TravelInstance.ShowSummary(inst, option, TravelRank)

print('******************************************************************************************')





