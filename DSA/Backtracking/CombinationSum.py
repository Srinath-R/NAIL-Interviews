class Solution(object):
    def combinationSum(self, candidates, target):
        """
        :type candidates: List[int]
        :type target: int
        :rtype: List[List[int]]
        """
        res = []
        candidates.sort()
        self.dfs(candidates, target, [], res)
        return res
    
    def dfs(self, candidates, target, path, res):
        if target < 0:
            return   #backtracking
        if target == 0:
            res.append(path)
            return
        for i in range(len(candidates)):
            self.dfs(candidates[i:], target - candidates[i], path + [candidates[i]], res)  
