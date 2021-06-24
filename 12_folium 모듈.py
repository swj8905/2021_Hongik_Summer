import folium

map = folium.Map(location=[36.621, 127.286], zoom_start=17)
map.save("./map.html")