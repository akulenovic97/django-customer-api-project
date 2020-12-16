from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.response import Response

from .models import Customer, Subscription, Gifts
from .serializers import CustomerSerializer, SubscriptionSerializer, GiftsSerializer
from rest_framework.decorators import api_view

# Create your views here.
@api_view(['POST', ])
def create_customer_view(request):
    #Assuming all POST requests will be a JSON request
    #Parse the JSON request into a Python dictionary
    try:
        all_data = JSONParser().parse(request)
    except Exception as e:
        return Response('Could not parse JSON POST request --> ' + str(e), status=status.HTTP_400_BAD_REQUEST)

    

    #Only dealing with POST method
    if request.method == 'POST':
        #Get only customer data from the request using dictionary comprehension
        customer_data = {key: value for key, value in all_data['customer'].items() if key not in ('subscription', 'gifts')}

        if len(all_data) < 1:
            return JsonResponse('No customer info to process, nothing to POST!', status=status.HTTP_400_BAD_REQUEST)
        elif len(all_data) == 1:
            customer_serializer = CustomerSerializer(data=customer_data)
        elif len(all_data) > 1:
            customer_serializer = CustomerSerializer(data=customer_data, many=True)

        #Check to see if the customer exists by cross-checking name and address but if it has a different ID
        #If so, this shouldn't be a POST request since we shouldn't be inserting this existing customer
        try:
            customer_db_data = Customer.objects.get(first_name=customer_data['first_name'], 
                                                    last_name=customer_data['last_name'],
                                                    address_1=customer_data['address_1'])
            #Get full names to compare between DB and the JSON                                        
            db_full_name = ' '.join([customer_db_data.first_name, customer_db_data.last_name])
            full_name = ' '.join([customer_data['first_name'], customer_data['last_name']])

            if full_name == db_full_name and str(customer_db_data.address_1).strip() == str(customer_data['address_1']).strip():
                return JsonResponse('Customer info seems to be a duplicate, please check the request...', safe=False, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            pass
        
        print('Past Customer Serializer')
        #Get Subscription data next
        subscription_data = all_data['customer']['subscription']
        #Check if we have more than one subscription
        if not all(isinstance(subscription_data, list) for s in subscription_data):
            print('Sub length is 1')
            subscription_serializer = SubscriptionSerializer(data=subscription_data)
        elif all(isinstance(subscription_data, list) for s in subscription_data):
            print('Sub length is more than 1')
            subscription_serializer = SubscriptionSerializer(data=subscription_data, many=True)
        print(subscription_data)
        print('\n')
        
        #Get Gift data next
        gifts_data = all_data['customer']['gifts']
        if not all(isinstance(gifts_data, list) for g in gifts_data):
            gifts_serializer = GiftsSerializer(data=gifts_data)
        elif all(isinstance(gifts_data, list) for g in gifts_data):
            gifts_serializer = GiftsSerializer(data=gifts_data, many=True)
        print(gifts_data)
        print('\n')
        
        #Try saving the serializers to the DB now (work from top to bottom)
        resp_data, error_flag = {}, False

        if customer_serializer.is_valid():
            customer_serializer.save()
            resp_data['customer'] = customer_serializer.data
        else:
            error_flag = True
            resp_data['customer'] = customer_serializer.errors

        if subscription_serializer.is_valid():
            subscription_serializer.save()
            resp_data['subscription'] = subscription_serializer.data
        else:
            error_flag = True
            resp_data['subscription'] = subscription_serializer.errors
        
        if gifts_serializer.is_valid():
            gifts_serializer.save()
            resp_data['gifts'] = gifts_serializer.data
        else:
            error_flag = True
            resp_data['gifts'] = gifts_serializer.errors

        if error_flag:
            return JsonResponse(resp_data, status = status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse(resp_data, status = status.HTTP_201_CREATED)
    
@api_view(['PUT', ])
def update_customer_view(request):
    #Parse the JSON request into a Python dictionary
    try:
        all_data = JSONParser().parse(request)
    except Exception as e:
        return Response('Could not parse JSON POST request --> ' + str(e), status=status.HTTP_400_BAD_REQUEST)

    #Try getting the corresponding Customer object from the DB
    try:
        customer_id = all_data['customer']['id']
        customer_obj = Customer.objects.get(id=customer_id)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    #For updates, we're assuming all of the JSON object will be passed so need to use PUT
    if request.method == 'PUT':
        resp_keys = ['customer', 'subscription', 'gifts']
        resp_data = {key: [] for key in resp_keys}

        #Get only customer data from the request using dictionary comprehension
        customer_data = {key: value for key, value in all_data['customer'].items() if key not in ('subscription', 'gifts')}

        if len(all_data) < 1:
            return JsonResponse('No customer info to process, nothing to PUT!', status=status.HTTP_400_BAD_REQUEST)
        elif len(all_data) == 1:
            customer_serializer = CustomerSerializer(customer_obj, data=customer_data)
        elif len(all_data) > 1:
            customer_serializer = CustomerSerializer(customer_obj, data=customer_data, many=True)
        
        #Check if there's subscription data to update
        try:
            #Get subscription data next
            sub_data = all_data['customer']['subscription']
            if not all(isinstance(sub_data, list) for s in sub_data):
                sub_obj = Subscription.objects.get(id=sub_data['id'])
                subscription_serializer = SubscriptionSerializer(sub_obj, sub_data)

                if subscription_serializer.is_valid():
                    subscription_serializer.save()
                    resp_data['subscription'].append(subscription_serializer.data)
                else:
                    error_flag = True
                    resp_data['subscription'].append(subscription_serializer.errors)
            else:
                for sub in sub_data:
                    #Get corresponding subscription from DB
                    print(sub)
                    sub_obj = Subscription.objects.get(id=sub['id'])
                    subscription_serializer = SubscriptionSerializer(sub_obj, data=sub)

                    if subscription_serializer.is_valid():
                        subscription_serializer.save()
                        resp_data['subscription'].append(subscription_serializer.data)
                    else:
                        error_flag = True
                        resp_data['subscription'].append(subscription_serializer.errors)
        except Exception as e:
            print('Could not update/get Subscription objects, moving on... ' + str(e))
        
        try:
            #Get Gift data next
            gifts_data = all_data['customer']['gifts']
            for gift in gifts_data:
                #Get corresponding gift from DB
                gifts_obj = Gifts.objects.get(id=gift['id'])
                gifts_serializer = GiftsSerializer(gifts_obj, data=gift)

                if gifts_serializer.is_valid():
                    gifts_serializer.save()
                    resp_data['gifts'].append(gifts_serializer.data)
                else:
                    error_flag = True
                    resp_data['gifts'].append(gifts_serializer.errors)
        except Exception as e:
            print('Could not update/get Gift objects, moving on... ' + str(e))
        
        #Try saving the serializers to the DB now (work from top to bottom)
        resp_data, error_flag = {}, False

        if customer_serializer.is_valid():
            customer_serializer.save()
            resp_data['customer'] = customer_serializer.data
        else:
            error_flag = True
            resp_data['customer'] = customer_serializer.errors

        if error_flag:
            return JsonResponse(resp_data, status = status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse(resp_data, status = status.HTTP_201_CREATED)


        

        

