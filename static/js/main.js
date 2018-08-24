var app = angular.module('orgDirectory', []);


var dir_ctrl =  function($scope, $http, $window) {
	$scope.records = [];
	$scope.enabledEdit = [];
	$scope.editState = false;
	$http.get("http://127.0.0.1:5000/v1/employee/")
      .then(function successCallback(response){
                $scope.records = response.data.records;
                console.log(response);
            }, function errorCallback(response){
                alert("Unable to fetch records. Try again later");
            });

    $scope.create_record = function(){
    	if (isEmpty($scope.name)){
	        alert("name should not be empty!")
	        return
      	}
      	if (isEmpty($scope.designation)){
	        alert("Designation should not be empty!")
	        return
      	}
      	if (isEmpty($scope.department)){
	        alert("Department should not be empty!")
	        return
      	}
      	var new_record = { name : $scope.name, designation: $scope.designation, department: $scope.department, manager_name: $scope.manager_name};
      	$http({
              method: 'POST',
              url: "http://127.0.0.1:5000/v1/employee/",
              data: new_record
            }).then(function successCallback(response) {
                        $window.location.reload();
                    }, function errorCallback(response) {
                        alert("Not able to insert new record. Please try again later");
                    });
    };

    $scope.search = function(){
    url = "http://127.0.0.1:5000/v1/employee/"+$scope.query;
      $http.get(url)
      .then(function successCallback(response){
                $scope.records = response.data.records;
                console.log(response);
            }, function errorCallback(response){
                console.log("Unable to search right now");
            });

    }

    $scope.editEmployee = function(index){
    	if($scope.editState){
    		$scope.editState = false;
    		var record = {name: $scope.records[index].name, designation:$scope.records[index].designation, department: $scope.records[index].department, manager_name:$scope.records[index].manager_name}
    		$http({
              method: 'POST',
              url: "http://127.0.0.1:5000/v1/employee/"+$scope.records[index].id,
              data: record
            }).then(function successCallback(response) {
            			alert("Record successfully deleted!");
                        $window.location.reload();
                    }, function errorCallback(response) {
                        alert("Something went wrong. Please try again later");
                    });
    	
    	}else{
    		$scope.enabledEdit[index] = true;
    		$scope.editState = true;
    		console.log("edit enabled");
    	}
    	

    }

    $scope.delete = function(id){
      
      $http({
              method: 'DELETE',
              url: "http://127.0.0.1:5000/v1/employee/"+id
            }).then(function successCallback(response) {
            			alert("Record successfully deleted!");
                        $window.location.reload();
                    }, function errorCallback(response) {
                        alert("Something went wrong. Please try again later");
                    });   
    }
    

    function isEmpty(str) {
        return (!str || 0 === str.length);
    }
    
};

app.controller('orgDirectoryCtrl', dir_ctrl);