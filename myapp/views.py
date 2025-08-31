from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Article
from .forms import ParseForm
from bs4 import BeautifulSoup
import requests
from datetime import datetime

# Функция для отображения списка новостей
def article_list(request):
    """Представление для отображения списка всех новостей"""
    articles = Article.objects.all().order_by('-published')
    return render(request, 'myapp/article_list.html', {'articles': articles})

# Функция для парсинга
def parse_news(request):
    """Универсальная функция парсинга для разных источников"""
    if request.method == 'POST':
        form = ParseForm(request.POST)
        if form.is_valid():
            source = form.cleaned_data['source']
            
            if source == 'lenta':
                return parse_lenta_news(request)
            elif source == 'rbc':
                return parse_rbc_news(request)
            else:
                messages.error(request, 'Неизвестный источник для парсинга')
                return redirect('parse_page')
    else:
        form = ParseForm()

    return render(request, 'myapp/parse.html', {'form': form})

def parse_lenta_news(request):
    """Парсинг Lenta.ru (адаптированная версия)"""
    url = 'https://lenta.ru/'
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        news_items = soup.find_all('a', class_='card-mini_topnews')
        print(f"Найдено новостей на Lenta.ru: {len(news_items)}")

        created_count = 0
        for item in news_items[:10]:
            try:
                title_elem = item.find('span', class_='card-mini__title')
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    
                    link = item.get('href', '')
                    if link.startswith('/'):
                        link = 'https://lenta.ru' + link
                    
                    if not Article.objects.filter(url=link).exists():
                        Article.objects.create(
                            title=title[:300],
                            url=link,
                            published=datetime.now(),
                            source='Lenta.ru',
                            text=title[:200]
                        )
                        created_count += 1
                        
            except Exception as e:
                print(f"Ошибка при обработке элемента Lenta: {e}")
                continue

        messages.success(request, f'Добавлено {created_count} новостей с Lenta.ru!')
        return redirect('article_list')

    except Exception as e:
        messages.error(request, f'Ошибка при парсинге Lenta.ru: {e}')
        return redirect('parse_page')

def parse_rbc_news(request):
    """Парсинг RBC.ru"""
    url = 'https://www.rbc.ru/short_news'
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Основные селекторы для RBC
        news_items = soup.find_all('div', class_='item__wrap')
        if not news_items:
            news_items = soup.find_all('a', class_='item__link')
        
        print(f"Найдено новостей на RBC.ru: {len(news_items)}")

        created_count = 0
        for item in news_items[:15]:
            try:
                # Ищем заголовок
                title_elem = item.find('span', class_='item__title')
                if not title_elem:
                    title_elem = item.find('div', class_='item__title')
                
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    
                    # Ищем ссылку
                    link_elem = item.find('a') if item.name != 'a' else item
                    link = link_elem.get('href', '') if link_elem else ''
                    
                    if link and not link.startswith('http'):
                        if link.startswith('/'):
                            link = 'https://www.rbc.ru' + link
                        else:
                            link = 'https://www.rbc.ru/' + link
                    
                    if link and not Article.objects.filter(url=link).exists():
                        Article.objects.create(
                            title=title[:300],
                            url=link,
                            published=datetime.now(),
                            source='RBC.ru',
                            text=title[:200]
                        )
                        created_count += 1
                        
            except Exception as e:
                print(f"Ошибка при обработке элемента RBC: {e}")
                continue

        messages.success(request, f'Добавлено {created_count} новостей с RBC.ru!')
        return redirect('article_list')

    except Exception as e:
        messages.error(request, f'Ошибка при парсинге RBC.ru: {e}')
        return redirect('parse_page')
