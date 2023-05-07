from rest_framework import serializers
from .models import Category, Product, Order, Comment


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    image = serializers.CharField()

    def create(self, validated_data):
        category = Category.objects.create(name=validated_data['name'], image=validated_data['image'])
        return category

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.image = validated_data['image']
        instance.save()
        return instance


class OrderSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.IntegerField(source='product.price', read_only=True)

    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        return order

    def update(self, instance, validated_data):
        pass

    class Meta:
        model = Order
        fields = ('id', 'product', 'product_name', 'product_price', 'date')
        # read_only_fields = ('name',)


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.IntegerField()
    category = serializers.IntegerField(source='category.id')
    image = serializers.CharField()

    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        return product

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

    #class Meta:
    #    model = Product
    #    fields = ('id', 'name', 'description', 'price', 'category', 'image')
        # read_only_fields = ('name',)


class Category2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'image')


class CategoryProductsSerializer(serializers.ModelSerializer):
    #vacancy = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    #vacancy = serializers.StringRelatedField(many=True, read_only=True)
    product = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'product')


class Product2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'category', 'image')
        # read_only_fields = ('name',)


class CommentSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        comment = Comment.objects.create(**validated_data)
        return comment

    class Meta:
        model = Comment
        fields = ('id', 'nickname', 'text', 'date', 'product')
        # read_only_fields = ('name',)


class ProductCommentSerializer(serializers.ModelSerializer):

    comment = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'comment')
