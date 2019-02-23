var threadVis = angular.module("threadVis", []);

threadVis.controller("threadControl", function threadControl($scope,$http){

	$scope.timeStep = 1;
	$scope.focusComment;
	$scope.allComments = [];	

	//$http.get('data/data_aqp015.json').then(
	$http.get('data/data_ar1drq.json').then(
		function(response){
			$scope.allComments = response.data;
			$scope.allComments.forEach(c => c.colour = intToRGB(hashCode(c.user)));			
			$scope.allComments.forEach(c =>{

				if (c.id2 == 1) c.depth = 0; // root
				parent = $scope.allComments.find(f => f.id2 == c.id_par2);
				c.depth = parent.depth + 1;
			})
			//console.log($scope.allComments);
			$scope.filterComments();

	});
		
	$scope.filterComments = function(){
		console.log($scope.timeStep);
		$scope.comments = $scope.allComments.filter(c => c.time == $scope.timeStep);

		//$scope.comments = $scope.comments.sort(function(a,b){ return a.id_par2-b.id_par2})
		//$scope.comments = $scope.comments.sort(function(a,b){ return a.id2-b.id2})
		$scope.comments = $scope.comments.sort(function(a,b){ return a.entry-b.entry})
		console.log($scope.comments.length + " comments filtered");
	}


	$scope.getCommentStyle = function(c){
		var s = {};
		s.width = c.comment.length/5 + 'px';
		s.left = c.depth * 10 + 'px';
		s['border-left'] = '10px solid #'+c.colour;
		return s;
	}

	$scope.focusThisComment = function(c){
		$scope.focusComment = c;
	}
})




function hashCode(str) { // java String#hashCode
    var hash = 0;
    for (var i = 0; i < str.length; i++) {
       hash = str.charCodeAt(i) + ((hash << 5) - hash);
    }
    return hash;
} 

function intToRGB(i){
    var c = (i & 0x00FFFFFF)
        .toString(16)
        .toUpperCase();

    return "00000".substring(0, 6 - c.length) + c;
}





		



