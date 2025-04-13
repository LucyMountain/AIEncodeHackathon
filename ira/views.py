from django.http import HttpResponse
from django.shortcuts import render

from format_text_data import format_text_data
from main import generate_investment_summary, start_init


# Create your views here.
def index(request):
    if request.method == "POST":
        city = request.POST.get('city')
        salary = int(request.POST.get('salary'))
        duration = int(request.POST.get('duration'))
        risk_tolerance = request.POST.get('risk_tolerance')
        preferred_types = []
        for i in ['Lending Platforms', 'DEXs', 'Yield Farming', 'Stablecoins', 'Staking', 'Vault Strategy', 'Auto Yield Aggregator']:
            if i in request.POST:
                preferred_types.append(i)
        summary = generate_investment_summary(city, salary, duration, risk_tolerance, preferred_types)
        user_inputs, monthly_amt, total_amt, investments = summary
        inv = []
        if investments:
            for name, type_, tvl, roi in investments:
                inv.append({'name': name, 'type': type_, 'tvl': round(tvl, 2), 'roi': round(roi, 2)})
        else:
            inv = False

    if request.headers.get('Hx-Request') == 'true':
        # return only the result to be replaced
        return render(request, 'ira/results.html', {'duration': duration, 'monthly_amt': monthly_amt, 'total_amt': total_amt, 'investments': inv})
    else:
        content = format_text_data()
        start_init()
        return render(request, 'ira/index.html', {'content': content})

