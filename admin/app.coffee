DragDirective = ->
  (scope, element, attrs) ->
    attrs.$set('draggable', true);

    data = attrs.jxDragData
    handler = attrs.jxDrag

    scope.$watch attrs.jxDrag, (value) => @handler = value
    element.bind "dragstart", (event) =>
      [dragData, dragTarget] = [data, event.target]
      event.dataTransfer.setData "text", dragData
      scope.dragTarget = dragTarget
      scope[handler]? dragData

DropDirective = ->
  (scope, element, attrs) ->
    element.bind "dragover", (event) ->
      event.preventDefault()

    data = attrs.jxDragData
    handler = attrs.jxDrop

    scope.$watch attrs.jxDrop, (value) => @handler = value
    element.bind "drop", (event) =>
      event.preventDefault()
      dragData = event.dataTransfer.getData "text"
      [dropData, dropTarget] = [data, event.target]
      scope.dropTarget = dropTarget
      scope[handler]? dragData, dropData

Admin = ($scope, $http, $timeout) ->
  $scope.converter = new Showdown.converter()

  $scope.drop = (from_id, to_id) ->
    from = $scope.dragTarget
    to = $scope.dropTarget
    if from != to && from_id && to_id
      $timeout ->
        $http.get("/_exchange?page1=" + from_id + "&page2=" + to_id).success ->
          [from.innerHTML, to.innerHTML] = [to.innerHTML, from.innerHTML]
        , 0.1

# Angular bootstrap
name = 'AdminPage'
app = angular.module name, []
app.controller 'Admin', Admin
app.directive 'jxDrag', DragDirective
app.directive 'jxDrop', DropDirective
angular.bootstrap document, [name]