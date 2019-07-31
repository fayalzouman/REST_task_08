from rest_framework import serializers
from django.contrib.auth.models import User
import datetime
from .models import Flight, Booking, Profile

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['first_name', 'last_name',]


class BookingSerializer(serializers.ModelSerializer):
	flight = serializers.SlugRelatedField(read_only=True, slug_field='destination')
	class Meta:
		model = Booking
		fields = ['flight', 'date', 'id']


class ProfileSerializer(serializers.ModelSerializer):
	past_bookings = serializers.SerializerMethodField()
	tier = serializers.SerializerMethodField()
	user = UserSerializer()
	class Meta:
		model = Profile
		fields = ['user', 'miles', 'past_bookings', 'tier',]

	def get_tier(self,obj):
		miles = obj.miles
		if miles >= 100000:
			return "Platinum"
		elif miles>=60000:
			return "Gold"
		elif miles>=10000:
			return "Silver"
		else:
			return "Blue"

	def get_past_bookings(self, obj):
		user_obj = obj.user
		booking_list = user_obj.bookings.filter(date__lt=datetime.date.today()) #bookings is from the related name in the Booking model
		return BookingSerializer(booking_list, many=True).data 


class FlightSerializer(serializers.ModelSerializer):
	class Meta:
		model = Flight
		fields = ['destination', 'time', 'price', 'id']


class BookingDetailsSerializer(serializers.ModelSerializer):
	flight = FlightSerializer()
	total = serializers.SerializerMethodField()
	class Meta:
		model = Booking
		fields = ['flight', 'date', 'passengers', 'id', 'total',]

	def get_total(self, obj):
		price_obj = obj.flight.price
		passengers_obj = obj.passengers
		total = price_obj * passengers_obj
		return total

class AdminUpdateBookingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Booking
		fields = ['date', 'passengers']


class UpdateBookingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Booking
		fields = ['passengers']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        new_user = User(username=username, first_name=first_name, last_name=last_name)
        new_user.set_password(password)
        new_user.save()
        return validated_data




