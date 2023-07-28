from rest_framework import serializers
from autoservices.database.models import tb_Category_Model

class TaskSerializer(serializers.ModelSerializer):
	class Meta:
		model = tb_Category_Model
		fields ='__all__'