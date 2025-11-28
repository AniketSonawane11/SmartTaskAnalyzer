from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import AnalyzeRequestSerializer, TaskModelSerializer
from .scoring import compute_scores
from .models import Task


# --------------------------
# POST /api/tasks/analyze/
# --------------------------
class AnalyzeTasksView(APIView):
    def post(self, request):
        serializer = AnalyzeRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=400)

        tasks = serializer.validated_data.get("tasks")
        strategy = serializer.validated_data.get("strategy", "smart_balance")

        results = compute_scores(tasks, strategy=strategy)
        return Response(results, status=200)



# --------------------------
# POST /api/tasks/suggest/
# --------------------------
class SuggestTasksView(APIView):

    def post(self, request):
        serializer = AnalyzeRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=400)

        tasks = serializer.validated_data.get("tasks")
        strategy = serializer.validated_data.get("strategy", "smart_balance")

        results = compute_scores(tasks, strategy=strategy)
        sorted_tasks = results["tasks"]

        top3 = sorted_tasks[:3]

        return Response(
            {
                "suggested_tasks": top3,
                "strategy_used": strategy,
                "cycles": results.get("cycles", []),
                "has_cycle": results.get("has_cycle", False),
            },
            status=200
        )

    # inside SuggestTasksView
def get(self, request):
    # read from DB and compute top3
    strategy = request.GET.get('strategy', 'smart_balance')
    tasks_qs = Task.objects.all().order_by('-created_at')
    tasks = TaskModelSerializer(tasks_qs, many=True).data
    results = compute_scores(tasks, strategy=strategy)
    top3 = results['tasks'][:3]
    return Response({
        'suggested_tasks': top3,
        'strategy_used': strategy,
        'has_cycle': results.get('has_cycle', False),
        'cycles': results.get('cycles', [])
    })




# --------------------------
# POST /api/tasks/add/
# --------------------------
class CreateTaskView(APIView):
    def post(self, request):
        serializer = TaskModelSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Task saved successfully", "task": serializer.data},
                status=201
            )
        
        return Response(serializer.errors, status=400)



# --------------------------
# GET /api/tasks/all/
# --------------------------
class ListTasksView(APIView):
    def get(self, request):
        tasks = Task.objects.all().order_by('-id')
        serializer = TaskModelSerializer(tasks, many=True)
        return Response(serializer.data)
