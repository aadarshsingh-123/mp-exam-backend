from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Avg, Max, Sum, Count, F, Window
from django.db.models.functions import Rank
from .models import TestResult, Question
from .serializers import TestResultSerializer, TestResultDetailSerializer, LeaderboardSerializer, QuestionSerializer


class SubmitTestView(generics.CreateAPIView):
    """Save a mock test result."""
    serializer_class = TestResultSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HistoryView(APIView):
    """Get current user's test history and stats."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        results = TestResult.objects.filter(user=request.user)
        stats = results.aggregate(
            total_tests=Count('id'),
            total_marks_obtained=Sum('obtained_marks'),
            total_marks_possible=Sum('total_marks'),
            average_percentage=Avg('percentage'),
            best_score=Max('percentage'),
            last_test_date=Max('created_at'),
        )
        # Handle None values
        for key in stats:
            if stats[key] is None:
                stats[key] = 0

        serializer = TestResultSerializer(results, many=True)
        return Response({
            'stats': stats,
            'results': serializer.data,
        })


class LeaderboardView(APIView):
    """Get top rankers for mock tests."""
    permission_classes = [AllowAny]

    def get(self, request):
        test_type = request.query_params.get('type', 'full')  # 'full' or 'subject'
        test_name = request.query_params.get('name', '')

        # Get the best score per user
        queryset = TestResult.objects.filter(test_type=test_type)
        if test_name:
            queryset = queryset.filter(test_name__icontains=test_name)

        # Get best attempt per user
        from django.db.models import OuterRef, Subquery
        best_per_user = (
            queryset
            .values('user')
            .annotate(best_pct=Max('percentage'))
            .order_by('-best_pct')
        )

        # Get the full results for the best attempts
        best_result_ids = []
        for entry in best_per_user[:50]:
            result = queryset.filter(
                user_id=entry['user'],
                percentage=entry['best_pct']
            ).first()
            if result:
                best_result_ids.append(result.id)

        top_results = TestResult.objects.filter(id__in=best_result_ids).select_related('user').order_by('-percentage', '-obtained_marks')

        data = []
        for rank, result in enumerate(top_results, 1):
            item = TestResultDetailSerializer(result).data
            item['rank'] = rank
            data.append(item)

        return Response(data)

class QuestionListView(generics.ListAPIView):
    """Fetch questions from backend. Filters by user's exam_type."""
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        queryset = Question.objects.all()
        category = self.request.query_params.get('category', None)
        limit = self.request.query_params.get('limit', None)
        
        # Filter by exam_type - use user's exam_type or query param
        exam_type = self.request.query_params.get('exam_type', None)
        if not exam_type:
            exam_type = getattr(self.request.user, 'exam_type', 'other')
        queryset = queryset.filter(exam_type=exam_type)

        if category and category != 'all':
            queryset = queryset.filter(category=category)

        if limit:
            try:
                limit = int(limit)
                queryset = queryset.order_by('?')[:limit]
            except ValueError:
                pass
        
        return queryset


class QuestionCategoriesView(APIView):
    """Get available question categories for the user's exam type."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        exam_type = request.query_params.get('exam_type', None)
        if not exam_type:
            exam_type = getattr(request.user, 'exam_type', 'other')
        
        categories = (
            Question.objects.filter(exam_type=exam_type)
            .values_list('category', flat=True)
            .distinct()
            .order_by('category')
        )
        
        category_data = []
        for cat in categories:
            count = Question.objects.filter(exam_type=exam_type, category=cat).count()
            category_data.append({'name': cat, 'count': count})
        
        return Response({
            'exam_type': exam_type,
            'categories': category_data,
            'total_questions': Question.objects.filter(exam_type=exam_type).count(),
        })
