# rest_framework kutubxonasi funksiya va classlar -> ...
from rest_framework.authtoken.models import Token
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
# django kutubxonasi funksiya va classlar -> ...
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db import IntegrityError
from django.shortcuts import render
# local applarning funksiya va classlari -> ...
from .models import Test
from .serializers import TestSerializer
# boshqa kutubxona, funksiyalar va classlar -> ...
import json, requests

class TestViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = TestSerializer
    queryset = Test.objects.all()

    def check(self, tests, code, language, timelimit):
        try:
            tests = eval(tests)
        except:
            tests = dict({})
        url = "https://algorithmshubrunapi.pythonanywhere.com/run/"
        token = "ba4afa78d6f27c17b1e9f30beac81857bb62c217"
        counter = 1
        cases = {}
        alltime = 0
        for test in tests:
            data = {
            "name": "author",
            "code": code,
            "userinput": str(test),
            "language": language
            }
            response = requests.post(
                url=url, 
                data=data,
                headers={
                    "Authorization": f"Token {token}"
                }
            )
            try:
                response = response.json()
            except:
                response = {"time": 0}
            # print("\n------------------------------\n",response, "---------------\n")
            if tests[test] == response["output"]:
                if float(response["time"]) > float(timelimit):
                    cases[f"test{counter}"] = {
                        "status": f"TimeLimit({counter})",
                        "time": response["time"]*1000,
                        "userinput": test,
                        "output": response["output"],
                        "error": response["error"]
                    }
                    counter += 1
                    alltime += response["time"]
                    break
                else:
                    cases[f"test{counter}"] = {
                        "status": "Accepted",
                        "time": response["time"]*1000,
                        "userinput": test,
                        "output": response["output"],
                        "error": response["error"]
                    }
                    counter += 1
                    alltime += response["time"]
                    continue
            else:
                if float(response["time"]) > float(timelimit):
                    cases[f"test{counter}"] = {
                        "status": f"TimeLimit({counter})",
                        "time": response["time"]*1000,
                        "userinput": test,
                        "output": response["output"],
                        "error": response["error"]
                    }
                    counter += 1
                    alltime += response["time"]
                    break
                if response["timelimit"]:
                    cases[f"test{counter}"] = {
                        "status": f"TimeLimit({counter})",
                        "time": response["time"]*1000,
                        "userinput": test,
                        "output": response["output"],
                        "error": response["error"]
                    }
                    counter += 1
                    alltime += response["time"]
                    break
                if response["error"] != " " and counter > 1 and not response["timelimit"]:
                    cases[f"test{counter}"] = {
                        "status": f"RunTimeError({counter})",
                        "time": response["time"]*1000,
                        "userinput": test,
                        "output": response["output"],
                        "error": response["error"]
                    }
                    counter += 1
                    alltime += response["time"]
                    break
                if response["error"] != " " and counter == 1 and not response["timelimit"]:
                    cases[f"test{counter}"] = {
                        "status": f"CompilationError({counter})",
                        "time": response["time"]*1000,
                        "userinput": test,
                        "output": response["output"],
                        "error": response["error"]
                    }
                    counter += 1
                    alltime += response["time"]
                    break
                if response["output"] != tests[test] and response["error"] == " " and not response["timelimit"]:
                    cases[f"test{counter}"] = {
                        "status": f"WrongAnswer({counter})",
                        "time": response["time"]*1000,
                        "userinput": test,
                        "output": response["output"],
                        "error": response["error"]
                    }
                    counter += 1
                    alltime += response["time"]
                    break
        cases["alltime"] = alltime/(counter-1)
        return cases


    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        tests = request.data.get("tests")
        results = self.check(tests=tests, code=request.data.get("code"), language=request.data.get("language"), timelimit=request.data.get("timelimit"))
        alltime = results.pop("alltime")
        request.data["nano"] = "alidev2005"
        request.data["author"] = "ali"
        request.data["tests"] = tests
        request.data["results"] = str(results)
        request.data["time"] = alltime*1000
        request.data["tielimit"] = request.data.get("timelimit")
        if type(request.data) != dict:
            request.data._mutable = False
        return super().create(request, *args, **kwargs)