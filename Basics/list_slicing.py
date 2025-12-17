#List Slicing Questions 

nums = [10, 20, 30, 40, 50, 60, 70] #QuestionNo1
print(nums[5:1:-1]) #[60,50,40,30]
print(nums[-2:2:-2]) #[60,40]
print(nums[100:]) #Blank

nums = [1, 2, 3, 4, 5] #QuestionNo2
nums[1:4] = [20, 30]#SubQuestion1
print(nums) #[1,20,30,5]
nums[::2] = [100, 200, 300]#SubQuestion2
print(nums) #[100,200,300,4,5]


