class Sorting:
    """
    In Progress
    """

    def __init__(self) -> None:
        pass

    def bubbleSort(nums):
        n = len(nums)

        for i in range(n):
            for j in range(n-i-1):
                if nums[j] > nums[j+1]:
                    nums[j],nums[j+1] = nums[j+1],nums[j]
                
        
        return nums