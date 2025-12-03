#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
北美华人社区、商家与旅游场景地图生成器
使用Python创建交互式地图
"""

import json
import os

# 地图数据
locations = {
    "communities": [
        {"name": "旧金山唐人街", "lat": 37.7946, "lng": -122.4094, "type": "community", 
         "desc": "北美最古老、规模最大的唐人街之一，拥有众多中餐馆、商店和文化景点"},
        {"name": "纽约曼哈顿唐人街", "lat": 40.7158, "lng": -73.9970, "type": "community", 
         "desc": "美国东海岸历史最悠久的华人聚居区，位于曼哈顿下城"},
        {"name": "纽约法拉盛", "lat": 40.7589, "lng": -73.8302, "type": "community", 
         "desc": "纽约市最大的华人社区之一，华人比例高达60%以上，商业繁荣"},
        {"name": "洛杉矶蒙特利公园", "lat": 34.0625, "lng": -118.1228, "type": "community", 
         "desc": "被誉为'第一座华人主导的美国城市'，华人比例超过60%"},
        {"name": "洛杉矶圣盖博", "lat": 34.0967, "lng": -118.1068, "type": "community", 
         "desc": "圣盖博谷核心城市，华人社区密集，商家林立"},
        {"name": "洛杉矶阿罕布拉", "lat": 34.0936, "lng": -118.1270, "type": "community", 
         "desc": "圣盖博谷重要华人聚居区，拥有大量华人商铺和餐馆"},
        {"name": "芝加哥唐人街", "lat": 41.8500, "lng": -87.6333, "type": "community", 
         "desc": "中西部地区重要的华人聚居地，以舍麦路和永活街为中心"},
        {"name": "波士顿唐人街", "lat": 42.3500, "lng": -71.0622, "type": "community", 
         "desc": "新英格兰地区唯一的唐人街，位于波士顿市中心"},
        {"name": "西雅图国际区", "lat": 47.5988, "lng": -122.3214, "type": "community", 
         "desc": "融合了华人、日本人和菲律宾人的文化，拥有中国牌坊"},
        {"name": "休斯顿亚洲城", "lat": 29.6900, "lng": -95.5028, "type": "community", 
         "desc": "德克萨斯州最大的华人社区，香港城购物中心是主要商业区"},
        {"name": "费城唐人街", "lat": 39.9526, "lng": -75.1552, "type": "community", 
         "desc": "位于费城市中心，拥有众多中餐馆和商铺"},
        {"name": "檀香山唐人街", "lat": 21.3099, "lng": -157.8581, "type": "community", 
         "desc": "美国最早的唐人街之一，位于夏威夷檀香山市"},
        {"name": "多伦多唐人街", "lat": 43.6532, "lng": -79.3972, "type": "community", 
         "desc": "位于多伦多市中心，沿登打士西街和士巴丹拿道延伸"},
        {"name": "多伦多万锦市", "lat": 43.8561, "lng": -79.3370, "type": "community", 
         "desc": "华人比例约62.8%，是加拿大华人聚居的主要城市之一"},
        {"name": "温哥华列治文市", "lat": 49.1666, "lng": -123.1364, "type": "community", 
         "desc": "华人占总人口的53%，被称为'小香港'，拥有大量华人商家"},
        {"name": "温哥华唐人街", "lat": 49.2794, "lng": -123.0986, "type": "community", 
         "desc": "北美第二大唐人街，位于温哥华市中心东部"}
    ],
    "restaurants": [
        {"name": "旧金山中餐馆集中区", "lat": 37.7946, "lng": -122.4094, "type": "restaurant", 
         "desc": "旧金山唐人街及周边，中餐馆密度极高"},
        {"name": "纽约中餐馆集中区", "lat": 40.7158, "lng": -73.9970, "type": "restaurant", 
         "desc": "曼哈顿唐人街和法拉盛，中餐馆数量众多"},
        {"name": "洛杉矶中餐馆集中区", "lat": 34.0625, "lng": -118.1228, "type": "restaurant", 
         "desc": "蒙特利公园、圣盖博、阿罕布拉等城市，中餐馆林立"},
        {"name": "多伦多中餐馆集中区", "lat": 43.6532, "lng": -79.3972, "type": "restaurant", 
         "desc": "多伦多唐人街及万锦市，中餐馆密集"},
        {"name": "温哥华中餐馆集中区", "lat": 49.1666, "lng": -123.1364, "type": "restaurant", 
         "desc": "列治文市和温哥华唐人街，中餐馆众多"}
    ],
    "shopping": [
        {"name": "南海岸广场", "lat": 33.6906, "lng": -117.8831, "type": "shopping", 
         "desc": "加州科斯塔梅萨，美国最大的购物中心之一，250家高端精品店，深受华人游客喜爱"},
        {"name": "梅西百货(纽约)", "lat": 40.7505, "lng": -73.9934, "type": "shopping", 
         "desc": "纽约曼哈顿，支持Alipay支付"},
        {"name": "Nordstrom(旧金山)", "lat": 37.7879, "lng": -122.4075, "type": "shopping", 
         "desc": "旧金山联合广场，支持Alipay支付"},
        {"name": "Saks Fifth Avenue", "lat": 40.7614, "lng": -73.9776, "type": "shopping", 
         "desc": "纽约第五大道，支持Alipay支付"},
        {"name": "Tory Burch", "lat": 40.7614, "lng": -73.9776, "type": "shopping", 
         "desc": "纽约第五大道，支持Alipay支付"},
        {"name": "Kate Spade", "lat": 40.7614, "lng": -73.9776, "type": "shopping", 
         "desc": "纽约第五大道，支持Alipay支付"},
        {"name": "联合广场(旧金山)", "lat": 37.7879, "lng": -122.4075, "type": "shopping", 
         "desc": "旧金山购物中心，汇集众多高端品牌"},
        {"name": "第五大道(纽约)", "lat": 40.7614, "lng": -73.9776, "type": "shopping", 
         "desc": "纽约奢侈品购物街，众多品牌支持Alipay"},
        {"name": "比佛利中心(洛杉矶)", "lat": 34.0736, "lng": -118.4004, "type": "shopping", 
         "desc": "洛杉矶比佛利山庄，高端购物中心"},
        {"name": "格罗夫购物中心(洛杉矶)", "lat": 34.0716, "lng": -118.3576, "type": "shopping", 
         "desc": "洛杉矶购物中心，汇集国际知名品牌"},
        {"name": "伊顿中心(多伦多)", "lat": 43.6532, "lng": -79.3806, "type": "shopping", 
         "desc": "多伦多最大的购物中心，汇集众多国际品牌"},
        {"name": "太古广场(多伦多)", "lat": 43.8561, "lng": -79.3370, "type": "shopping", 
         "desc": "北美最大的亚洲购物中心之一，位于万锦市"},
        {"name": "时代坊(温哥华)", "lat": 49.1666, "lng": -123.1364, "type": "shopping", 
         "desc": "温哥华列治文市，提供丰富的亚洲商品"},
        {"name": "太平洋中心(温哥华)", "lat": 49.2794, "lng": -123.1189, "type": "shopping", 
         "desc": "温哥华主要购物中心，汇集众多国际品牌"},
        {"name": "香港城购物中心(休斯顿)", "lat": 29.6900, "lng": -95.5028, "type": "shopping", 
         "desc": "休斯顿亚洲城，主要的购物和餐饮中心"},
        {"name": "休斯顿购物中心", "lat": 29.7500, "lng": -95.4619, "type": "shopping", 
         "desc": "休斯顿市中心，汇集众多国际品牌"},
        {"name": "科普利广场(波士顿)", "lat": 42.3500, "lng": -71.0756, "type": "shopping", 
         "desc": "波士顿主要购物中心，汇集众多高端品牌"},
        {"name": "密歇根大道(芝加哥)", "lat": 41.9000, "lng": -87.6247, "type": "shopping", 
         "desc": "芝加哥主要购物街，汇集众多奢侈品牌"},
        {"name": "西湖中心(西雅图)", "lat": 47.6097, "lng": -122.3331, "type": "shopping", 
         "desc": "西雅图市中心购物中心，汇集众多国际品牌"},
        {"name": "拉斯维加斯大道", "lat": 36.1147, "lng": -115.1728, "type": "shopping", 
         "desc": "汇集众多奢侈品牌店和娱乐设施，华人游客喜爱的消费场所"}
    ],
    "tourism": [
        {"name": "金门大桥", "lat": 37.8199, "lng": -122.4783, "type": "tourism", 
         "desc": "旧金山标志性景点，每年吸引大量游客"},
        {"name": "自由女神像", "lat": 40.6892, "lng": -74.0445, "type": "tourism", 
         "desc": "纽约标志性景点，华人游客必访"},
        {"name": "时代广场", "lat": 40.7580, "lng": -73.9855, "type": "tourism", 
         "desc": "纽约著名景点，购物和娱乐中心"},
        {"name": "好莱坞星光大道", "lat": 34.1016, "lng": -118.3268, "type": "tourism", 
         "desc": "洛杉矶著名景点，华人游客必访"},
        {"name": "比佛利山庄", "lat": 34.0736, "lng": -118.4004, "type": "tourism", 
         "desc": "洛杉矶高端购物和旅游区"},
        {"name": "CN塔(多伦多)", "lat": 43.6426, "lng": -79.3871, "type": "tourism", 
         "desc": "多伦多标志性建筑，华人游客必访"},
        {"name": "斯坦利公园(温哥华)", "lat": 49.3000, "lng": -123.1417, "type": "tourism", 
         "desc": "温哥华著名景点，吸引大量游客"},
        {"name": "太空针塔(西雅图)", "lat": 47.6205, "lng": -122.3493, "type": "tourism", 
         "desc": "西雅图标志性建筑，华人游客必访"},
        {"name": "千禧公园(芝加哥)", "lat": 41.8825, "lng": -87.6244, "type": "tourism", 
         "desc": "芝加哥著名景点，吸引大量游客"},
        {"name": "哈佛大学", "lat": 42.3770, "lng": -71.1167, "type": "tourism", 
         "desc": "波士顿著名学府，吸引大量华人游客和学生"}
    ],
    "alipay": [
        {"name": "Target(部分门店)", "lat": 40.7589, "lng": -73.8302, "type": "alipay", 
         "desc": "支持Alipay支付的大型零售商"},
        {"name": "CVS Pharmacy(部分门店)", "lat": 40.7589, "lng": -73.8302, "type": "alipay", 
         "desc": "支持Alipay支付的连锁药店"},
        {"name": "机场免税店", "lat": 40.6413, "lng": -73.7781, "type": "alipay", 
         "desc": "JFK、LAX、SFO等主要机场，支持Alipay支付"}
    ],
    "universities": [
        {"name": "哈佛大学", "lat": 42.3770, "lng": -71.1167, "type": "university", 
         "desc": "马萨诸塞州，大量中国留学生"},
        {"name": "MIT", "lat": 42.3601, "lng": -71.0942, "type": "university", 
         "desc": "马萨诸塞州，大量中国留学生"},
        {"name": "斯坦福大学", "lat": 37.4275, "lng": -122.1697, "type": "university", 
         "desc": "加州，大量中国留学生"},
        {"name": "UC Berkeley", "lat": 37.8719, "lng": -122.2585, "type": "university", 
         "desc": "加州，大量中国留学生"},
        {"name": "UCLA", "lat": 34.0689, "lng": -118.4452, "type": "university", 
         "desc": "加州，大量中国留学生"},
        {"name": "哥伦比亚大学", "lat": 40.8075, "lng": -73.9626, "type": "university", 
         "desc": "纽约，大量中国留学生"},
        {"name": "NYU", "lat": 40.7295, "lng": -73.9965, "type": "university", 
         "desc": "纽约，大量中国留学生"},
        {"name": "多伦多大学", "lat": 43.6532, "lng": -79.3832, "type": "university", 
         "desc": "多伦多，大量中国留学生"},
        {"name": "UBC", "lat": 49.2606, "lng": -123.2460, "type": "university", 
         "desc": "温哥华，大量中国留学生"}
    ]
}

# 图标颜色 - 优化后的配色方案，提高对比度和可读性
icon_colors = {
    "chinese_community": "#E53935",      # 红色 - 华人社区/唐人街（更鲜艳的红色）
    "asian_community": "#FF6B35",        # 橙红色 - 其他亚洲社区（日韩、东南亚、南亚等）
    "restaurant": "#1E88E5",             # 蓝色 - 亚洲餐厅（更亮的蓝色）
    "shopping": "#43A047",               # 绿色 - 购物中心（更饱和的绿色）
    "tourism": "#FB8C00",                # 橙色 - 旅游景点（更亮的橙色）
    "alipay": "#8E24AA",                 # 紫色 - Alipay商户（更深的紫色）
    "university": "#039BE5"              # 天蓝色 - 大学（更鲜明的蓝色）
}

# 图标名称映射
icon_names = {
    "chinese_community": "华人社区/唐人街",
    "asian_community": "日韩东南亚社区",
    "restaurant": "亚洲餐厅集中区",
    "shopping": "购物中心/消费品牌店",
    "tourism": "旅游景点",
    "alipay": "接入Alipay的代表性商户品牌",
    "university": "大学/教育机构"
}

# 标记大小映射 - 根据类型设置不同大小
marker_sizes = {
    "chinese_community": 12,
    "asian_community": 12,
    "restaurant": 10,
    "shopping": 11,
    "tourism": 13,
    "alipay": 9,
    "university": 14
}

# 图标符号映射 - 为不同类型使用不同符号
icon_symbols = {
    "chinese_community": "🏘️",
    "asian_community": "🌏",
    "restaurant": "🍜",
    "shopping": "🛍️",
    "tourism": "🗺️",
    "alipay": "💳",
    "university": "🎓"
}

def create_map_with_folium():
    """使用folium创建地图"""
    try:
        import folium
        
        # 创建地图，居中显示北美
        m = folium.Map(
            location=[40.0, -95.0],
            zoom_start=4,
            tiles='CartoDB positron'  # 使用简洁的地图样式
        )
        
        # 统计信息 - 按类型统计
        type_stats = {}
        for category, items in locations.items():
            for item in items:
                type_name = item['type']
                type_stats[type_name] = type_stats.get(type_name, 0) + 1
        total_locations = sum(type_stats.values())
        
        # 按类型分组创建图层组
        layer_groups = {}
        for type_name in icon_colors.keys():
            layer_groups[type_name] = folium.FeatureGroup(name=icon_names[type_name])
        
        # 添加所有标记点
        for category, items in locations.items():
            for item in items:
                color = icon_colors.get(item['type'], '#666666')
                size = marker_sizes.get(item['type'], 10)
                symbol = icon_symbols.get(item['type'], '📍')
                
                # 创建美观的popup内容
                popup_html = f'''
                <div style="font-family: 'Microsoft YaHei', Arial, sans-serif; min-width: 250px;">
                    <div style="background: linear-gradient(135deg, {color} 0%, {color}dd 100%);
                                color: white; padding: 12px; border-radius: 8px 8px 0 0; margin: -10px -10px 10px -10px;">
                        <h3 style="margin: 0; font-size: 16px; font-weight: bold;">
                            {symbol} {item['name']}
                        </h3>
                    </div>
                    <div style="padding: 8px 0;">
                        <p style="margin: 8px 0; color: #555; line-height: 1.6; font-size: 14px;">
                            <strong>类型：</strong><span style="color: {color}; font-weight: bold;">
                            {icon_names[item['type']]}</span>
                        </p>
                        <p style="margin: 8px 0; color: #666; line-height: 1.6; font-size: 13px;">
                            {item['desc']}
                        </p>
                        <p style="margin: 8px 0; color: #888; font-size: 12px;">
                            📍 坐标: {item['lat']:.4f}, {item['lng']:.4f}
                        </p>
                    </div>
                </div>
                '''
                
                folium.CircleMarker(
                    location=[item['lat'], item['lng']],
                    radius=size,
                    popup=folium.Popup(popup_html, max_width=300),
                    tooltip=f"{symbol} {item['name']}",
                    color='white',
                    weight=2.5,
                    fillColor=color,
                    fillOpacity=0.85
                ).add_to(layer_groups[item['type']])
        
        # 将所有图层组添加到地图
        for layer_group in layer_groups.values():
            layer_group.add_to(m)
        
        # 添加图层控制
        folium.LayerControl(collapsed=False).add_to(m)
        
        # 添加统计信息面板
        stats_html = f'''
        <div style="position: fixed; 
                    top: 10px; right: 10px; width: 220px; height: auto; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white; z-index:9999; font-size:13px;
                    border-radius:10px; padding: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);
                    font-family: 'Microsoft YaHei', Arial, sans-serif;">
            <h3 style="margin: 0 0 12px 0; font-size: 16px; font-weight: bold; text-align: center;">
                📊 数据统计
            </h3>
            <div style="background: rgba(255,255,255,0.2); border-radius: 6px; padding: 8px; margin-bottom: 8px;">
                <div style="font-size: 20px; font-weight: bold; text-align: center;">
                    {total_locations}
                </div>
                <div style="font-size: 11px; text-align: center; opacity: 0.9;">
                    总地点数
                </div>
            </div>
        '''
        for type_name in sorted(icon_colors.keys()):
            count = type_stats.get(type_name, 0)
            if count > 0:
                color = icon_colors.get(type_name, '#666666')
                symbol = icon_symbols.get(type_name, '📍')
                stats_html += f'''
                <div style="display: flex; justify-content: space-between; align-items: center;
                            padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.2);">
                    <span>{symbol} {icon_names[type_name]}</span>
                    <span style="font-weight: bold; background: rgba(255,255,255,0.3); 
                                 padding: 2px 8px; border-radius: 12px;">{count}</span>
                </div>
                '''
        stats_html += '</div>'
        m.get_root().html.add_child(folium.Element(stats_html))
        
        # 添加美化的图例
        legend_html = '''
        <div style="position: fixed; 
                    bottom: 50px; right: 10px; width: 240px; height: auto; 
                    background: white; z-index:9999; font-size:13px;
                    border:2px solid #ddd; border-radius:10px; padding: 15px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.2);
                    font-family: 'Microsoft YaHei', Arial, sans-serif;">
        <h4 style="margin: 0 0 12px 0; font-size: 15px; font-weight: bold; 
                   color: #333; border-bottom: 2px solid #eee; padding-bottom: 8px;">
            🗺️ 图例说明
        </h4>
        '''
        for type_name, color in icon_colors.items():
            symbol = icon_symbols.get(type_name, '📍')
            legend_html += f'''
            <div style="display: flex; align-items: center; padding: 6px 0;">
                <div style="width: 16px; height: 16px; background-color: {color}; 
                           border-radius: 50%; border: 2px solid white; 
                           box-shadow: 0 0 0 1px #ddd; margin-right: 10px;"></div>
                <span style="color: #555;">{symbol} {icon_names[type_name]}</span>
            </div>
            '''
        legend_html += '</div>'
        m.get_root().html.add_child(folium.Element(legend_html))
        
        # 保存地图
        output_file = 'north_america_chinese_communities_map_folium.html'
        m.save(output_file)
        print(f"✅ Folium地图已保存: {output_file}")
        return True
        
    except ImportError:
        print("❌ folium未安装，尝试安装: pip install folium")
        return False

def create_map_with_plotly(return_fig=False):
    """使用plotly创建地图
    
    Args:
        return_fig: 如果为True，返回figure对象而不是保存文件
    
    Returns:
        如果return_fig=True，返回plotly figure对象；否则返回True/False表示是否成功
    """
    try:
        import plotly.graph_objects as go
        import plotly.express as px
        
        # 准备数据
        all_locations = []
        for category, items in locations.items():
            for item in items:
                symbol = icon_symbols.get(item['type'], '📍')
                all_locations.append({
                    'name': item['name'],
                    'lat': item['lat'],
                    'lng': item['lng'],
                    'type': item['type'],
                    'desc': item['desc'],
                    'color': icon_colors[item['type']],
                    'symbol': symbol,
                    'type_name': icon_names[item['type']]
                })
        
        # 统计信息 - 按类型统计而不是按类别
        type_stats = {}
        for loc in all_locations:
            type_name = loc['type']
            type_stats[type_name] = type_stats.get(type_name, 0) + 1
        total_locations = len(all_locations)
        
        # 创建地图
        fig = go.Figure()
        
        # 按类型分组添加标记
        for type_name, color in icon_colors.items():
            type_locations = [loc for loc in all_locations if loc['type'] == type_name]
            if type_locations:
                size = marker_sizes.get(type_name, 10)
                symbol = icon_symbols.get(type_name, '📍')
                
                # 创建丰富的hover信息
                hover_texts = []
                for loc in type_locations:
                    hover_text = f"""
                    <b style='color: {color}; font-size: 16px;'>{loc['symbol']} {loc['name']}</b><br>
                    <span style='color: #666;'>类型：</span><b>{loc['type_name']}</b><br>
                    <span style='color: #666;'>{loc['desc']}</span><br>
                    <span style='color: #999; font-size: 11px;'>📍 {loc['lat']:.4f}, {loc['lng']:.4f}</span>
                    """
                    hover_texts.append(hover_text)
                
                fig.add_trace(go.Scattergeo(
                    lon=[loc['lng'] for loc in type_locations],
                    lat=[loc['lat'] for loc in type_locations],
                    text=[f"{loc['symbol']} {loc['name']}" for loc in type_locations],
                    mode='markers',
                    marker=dict(
                        size=size * 1.5,  # 放大标记以便更清晰
                        color=color,
                        line=dict(width=2.5, color='white'),
                        opacity=0.85
                    ),
                    name=f"{symbol} {icon_names[type_name]}",
                    hovertemplate='%{hovertext}<extra></extra>',
                    hovertext=hover_texts,
                    showlegend=True
                ))
        
        # 设置地图布局 - 使用更详细的地图样式
        fig.update_geos(
            projection_type="mercator",
            center=dict(lat=40, lon=-95),
            scope="north america",
            # 陆地、海洋、湖泊
            showland=True,
            landcolor="rgb(245, 245, 240)",  # 浅米色陆地，更自然
            showocean=True,
            oceancolor="rgb(230, 245, 255)",  # 浅蓝色海洋
            showlakes=True,
            lakecolor="rgb(200, 230, 255)",  # 浅蓝色湖泊
            showrivers=True,
            rivercolor="rgb(180, 220, 255)",  # 浅蓝色河流
            # 边界线
            coastlinecolor="rgb(80, 80, 80)",  # 深灰色海岸线
            coastlinewidth=1.5,
            showcountries=True,
            countrycolor="rgb(120, 120, 120)",  # 深灰色国家边界
            countrywidth=2,
            # 添加框架
            showframe=True,
            framecolor="rgb(100, 100, 100)",
            framewidth=1.5,
            # 分辨率设置（更详细）
            resolution=50  # 使用中等分辨率，显示更多细节
        )
        
        # 创建统计信息文本 - 使用类型名称，放大字体
        stats_text = f"<b style='font-size: 18px; color: #2c3e50;'>总地点数: {total_locations}</b><br><br>"
        for type_name in sorted(icon_colors.keys()):
            count = type_stats.get(type_name, 0)
            if count > 0:
                symbol = icon_symbols.get(type_name, '📍')
                stats_text += f"<span style='font-size: 15px;'>{symbol} {icon_names[type_name]}: {count}</span><br>"
        
        # 添加美国主要州名标注（使用州的地理中心坐标）
        us_states = [
            {"name": "CA", "lat": 36.7783, "lng": -119.4179},
            {"name": "NY", "lat": 42.1657, "lng": -74.9481},
            {"name": "TX", "lat": 31.0545, "lng": -97.5635},
            {"name": "FL", "lat": 27.7663, "lng": -81.6868},
            {"name": "IL", "lat": 40.3495, "lng": -88.9861},
            {"name": "MA", "lat": 42.2373, "lng": -71.5314},
            {"name": "WA", "lat": 47.0379, "lng": -120.5015},
            {"name": "PA", "lat": 40.5908, "lng": -77.2098},
            {"name": "HI", "lat": 21.3099, "lng": -157.8581},
            {"name": "NV", "lat": 38.3135, "lng": -117.0554},
            {"name": "AZ", "lat": 34.0489, "lng": -111.0937},
            {"name": "GA", "lat": 32.1656, "lng": -82.9001},
            {"name": "NC", "lat": 35.5397, "lng": -79.8431},
            {"name": "MI", "lat": 43.3266, "lng": -84.5361},
            {"name": "OH", "lat": 40.3888, "lng": -82.7649},
            {"name": "NJ", "lat": 40.2989, "lng": -74.5210},
            {"name": "VA", "lat": 37.7693, "lng": -78.1697},
            {"name": "OR", "lat": 43.8041, "lng": -120.5542},
            {"name": "CT", "lat": 41.5978, "lng": -72.7554},
            {"name": "CO", "lat": 39.0598, "lng": -105.3111},
        ]
        
        # 添加州名文本标注
        for state in us_states:
            fig.add_trace(go.Scattergeo(
                lon=[state['lng']],
                lat=[state['lat']],
                text=[state['name']],
                mode='text',
                textfont=dict(
                    size=10,
                    color='#666666',
                    family='Arial, sans-serif'
                ),
                showlegend=False,
                hoverinfo='skip'
            ))
        
        fig.update_layout(
            height=900,
            geo=dict(
                lonaxis_range=[-170, -50],
                lataxis_range=[15, 70],
                bgcolor='rgba(0,0,0,0)'
            ),
            legend=dict(
                yanchor="top",
                y=0.95,
                xanchor="left",
                x=0.005,  # 往左移动（从0.02减小到0.015，约5px的偏移）
                bgcolor="rgba(255, 255, 255, 0.92)",
                bordercolor="rgba(0, 0, 0, 0.3)",
                borderwidth=2,
                font=dict(size=15, family='Microsoft YaHei, Arial, sans-serif'),  # 放大字体
                itemclick="toggleothers",
                itemdoubleclick="toggle",
                title=dict(
                    text="<b style='font-size: 18px;'>图例</b>",
                    font=dict(size=18, color='#2c3e50')
                )
            ),
            paper_bgcolor='white',
            plot_bgcolor='white',
            margin=dict(l=0, r=0, t=0, b=0)
        )
        
        # 添加标题注释 - 直接嵌入到地图画布中
        fig.add_annotation(
            text="<b style='font-size: 22px; color: #2c3e50;'>🗺️ 北美华人社区、商家与旅游场景地图</b>",
            xref="paper", yref="paper",
            x=0.5, y=0.98,
            xanchor="center", yanchor="top",
            bgcolor="rgba(255, 255, 255, 0.92)",
            bordercolor="rgba(0, 0, 0, 0.3)",
            borderwidth=2,
            borderpad=12,
            font=dict(size=18, family='Microsoft YaHei, Arial, sans-serif', color='#2c3e50'),
            showarrow=False,
            align="center"
        )
        
        # 添加统计信息注释 - 移到左侧，放在图例下方
        fig.add_annotation(
            text=stats_text,
            xref="paper", yref="paper",
            x=0.1, y=0.65,  # 往左移动，与图例对齐（从0.02减小到0.015）
            xanchor="left", yanchor="top",
            bgcolor="rgba(255, 255, 255, 0.92)",
            bordercolor="rgba(0, 0, 0, 0.3)",
            borderwidth=2,
            borderpad=12,
            font=dict(size=14, family='Microsoft YaHei, Arial, sans-serif', color='#2c3e50'),  # 放大字体
            showarrow=False,
            align="left"
        )
        
        # 如果只需要返回figure对象（用于Streamlit等），直接返回
        if return_fig:
            return fig
        
        # 否则保存地图文件
        output_file = 'north_america_chinese_communities_map_plotly.html'
        fig.write_html(output_file, config={'displayModeBar': True, 'displaylogo': False})
        print(f"✅ Plotly地图已保存: {output_file}")
        return True
        
    except ImportError:
        if return_fig:
            return None
        print("❌ plotly未安装，尝试安装: pip install plotly")
        return False

# 全亚洲场景数据（包括华人社区和其他亚洲社区）
asia_locations = {
    "chinese_communities": [
        {"name": "旧金山唐人街", "lat": 37.7946, "lng": -122.4094, "type": "chinese_community", 
         "desc": "北美最古老、规模最大的唐人街之一，拥有众多中餐馆、商店和文化景点"},
        {"name": "纽约曼哈顿唐人街", "lat": 40.7158, "lng": -73.9970, "type": "chinese_community", 
         "desc": "美国东海岸历史最悠久的华人聚居区，位于曼哈顿下城"},
        {"name": "纽约法拉盛", "lat": 40.7589, "lng": -73.8302, "type": "chinese_community", 
         "desc": "纽约市最大的华人社区之一，华人比例高达60%以上，商业繁荣"},
        {"name": "洛杉矶蒙特利公园", "lat": 34.0625, "lng": -118.1228, "type": "chinese_community", 
         "desc": "被誉为'第一座华人主导的美国城市'，华人比例超过60%"},
        {"name": "洛杉矶圣盖博", "lat": 34.0967, "lng": -118.1068, "type": "chinese_community", 
         "desc": "圣盖博谷核心城市，华人社区密集，商家林立"},
        {"name": "洛杉矶阿罕布拉", "lat": 34.0936, "lng": -118.1270, "type": "chinese_community", 
         "desc": "圣盖博谷重要华人聚居区，拥有大量华人商铺和餐馆"},
        {"name": "芝加哥唐人街", "lat": 41.8500, "lng": -87.6333, "type": "chinese_community", 
         "desc": "中西部地区重要的华人聚居地，以舍麦路和永活街为中心"},
        {"name": "波士顿唐人街", "lat": 42.3500, "lng": -71.0622, "type": "chinese_community", 
         "desc": "新英格兰地区唯一的唐人街，位于波士顿市中心"},
        {"name": "费城唐人街", "lat": 39.9526, "lng": -75.1552, "type": "chinese_community", 
         "desc": "位于费城市中心，拥有众多中餐馆和商铺"},
        {"name": "檀香山唐人街", "lat": 21.3099, "lng": -157.8581, "type": "chinese_community", 
         "desc": "美国最早的唐人街之一，位于夏威夷檀香山市"},
        {"name": "多伦多唐人街", "lat": 43.6532, "lng": -79.3972, "type": "chinese_community", 
         "desc": "位于多伦多市中心，沿登打士西街和士巴丹拿道延伸"},
        {"name": "多伦多万锦市", "lat": 43.8561, "lng": -79.3370, "type": "chinese_community", 
         "desc": "华人比例约62.8%，是加拿大华人聚居的主要城市之一"},
        {"name": "温哥华列治文市", "lat": 49.1666, "lng": -123.1364, "type": "chinese_community", 
         "desc": "华人占总人口的53%，被称为'小香港'，拥有大量华人商家"},
        {"name": "温哥华唐人街", "lat": 49.2794, "lng": -123.0986, "type": "chinese_community", 
         "desc": "北美第二大唐人街，位于温哥华市中心东部"},
        {"name": "休斯顿亚洲城", "lat": 29.6900, "lng": -95.5028, "type": "chinese_community", 
         "desc": "德克萨斯州最大的华人社区，香港城购物中心是主要商业区"},
    ],
    "asian_communities": [
        {"name": "小东京(洛杉矶)", "lat": 34.0500, "lng": -118.2386, "type": "asian_community", 
         "desc": "洛杉矶日本社区，日式餐厅和商店集中"},
        {"name": "韩国城(洛杉矶)", "lat": 34.0578, "lng": -118.3006, "type": "asian_community", 
         "desc": "洛杉矶韩国社区，韩式餐厅和KTV集中"},
        {"name": "小印度(纽约)", "lat": 40.7505, "lng": -73.9934, "type": "asian_community", 
         "desc": "纽约印度社区，印度餐厅和商店集中"},
        {"name": "小西贡(橙县)", "lat": 33.7879, "lng": -117.8531, "type": "asian_community", 
         "desc": "加州橙县越南社区，越南餐厅和商店集中"},
        {"name": "小马尼拉(洛杉矶)", "lat": 34.0522, "lng": -118.2437, "type": "asian_community", 
         "desc": "洛杉矶菲律宾社区，菲律宾餐厅和商店集中"},
        {"name": "小泰国(洛杉矶)", "lat": 34.1016, "lng": -118.3268, "type": "asian_community", 
         "desc": "洛杉矶泰国社区，泰式餐厅和商店集中"},
        {"name": "日本城(旧金山)", "lat": 37.7850, "lng": -122.4297, "type": "asian_community", 
         "desc": "旧金山日本社区，日式餐厅和商店集中"},
        {"name": "韩国城(多伦多)", "lat": 43.6532, "lng": -79.3832, "type": "asian_community", 
         "desc": "多伦多韩国社区，韩式餐厅和商店集中"},
        {"name": "小印度(多伦多)", "lat": 43.6532, "lng": -79.3832, "type": "asian_community", 
         "desc": "多伦多印度社区，印度餐厅和商店集中"},
        {"name": "小西贡(温哥华)", "lat": 49.1666, "lng": -123.1364, "type": "asian_community", 
         "desc": "温哥华越南社区，越南餐厅和商店集中"},
        {"name": "小马尼拉(温哥华)", "lat": 49.1666, "lng": -123.1364, "type": "asian_community", 
         "desc": "温哥华菲律宾社区，菲律宾餐厅和商店集中"},
        {"name": "小东京(西雅图)", "lat": 47.6097, "lng": -122.3331, "type": "asian_community", 
         "desc": "西雅图日本社区，日式餐厅和商店集中"},
        {"name": "韩国城(芝加哥)", "lat": 41.8500, "lng": -87.6333, "type": "asian_community", 
         "desc": "芝加哥韩国社区，韩式餐厅和商店集中"},
        {"name": "小印度(芝加哥)", "lat": 41.8500, "lng": -87.6333, "type": "asian_community", 
         "desc": "芝加哥印度社区，印度餐厅和商店集中"},
        {"name": "小西贡(休斯顿)", "lat": 29.6900, "lng": -95.5028, "type": "asian_community", 
         "desc": "休斯顿越南社区，越南餐厅和商店集中"},
        {"name": "小马尼拉(休斯顿)", "lat": 29.6900, "lng": -95.5028, "type": "asian_community", 
         "desc": "休斯顿菲律宾社区，菲律宾餐厅和商店集中"},
        {"name": "西雅图国际区", "lat": 47.5988, "lng": -122.3214, "type": "asian_community", 
         "desc": "融合了华人、日本人和菲律宾人的文化，拥有中国牌坊"},
    ],
    "restaurants": [
        {"name": "日式餐厅集中区(洛杉矶)", "lat": 34.0500, "lng": -118.2386, "type": "restaurant", 
         "desc": "小东京及周边，日式餐厅密度极高"},
        {"name": "韩式餐厅集中区(洛杉矶)", "lat": 34.0578, "lng": -118.3006, "type": "restaurant", 
         "desc": "韩国城及周边，韩式餐厅数量众多"},
        {"name": "印度餐厅集中区(纽约)", "lat": 40.7505, "lng": -73.9934, "type": "restaurant", 
         "desc": "小印度及周边，印度餐厅密集"},
        {"name": "泰式餐厅集中区(洛杉矶)", "lat": 34.1016, "lng": -118.3268, "type": "restaurant", 
         "desc": "小泰国及周边，泰式餐厅林立"},
        {"name": "越南餐厅集中区(橙县)", "lat": 33.7879, "lng": -117.8531, "type": "restaurant", 
         "desc": "小西贡及周边，越南餐厅密集"},
        {"name": "菲律宾餐厅集中区(洛杉矶)", "lat": 34.0522, "lng": -118.2437, "type": "restaurant", 
         "desc": "小马尼拉及周边，菲律宾餐厅众多"},
        {"name": "日式餐厅集中区(旧金山)", "lat": 37.7850, "lng": -122.4297, "type": "restaurant", 
         "desc": "日本城及周边，日式餐厅密集"},
        {"name": "韩式餐厅集中区(多伦多)", "lat": 43.6532, "lng": -79.3832, "type": "restaurant", 
         "desc": "韩国城及周边，韩式餐厅密集"},
        {"name": "印度餐厅集中区(多伦多)", "lat": 43.6532, "lng": -79.3832, "type": "restaurant", 
         "desc": "小印度及周边，印度餐厅密集"},
        {"name": "亚洲餐厅集中区(温哥华)", "lat": 49.1666, "lng": -123.1364, "type": "restaurant", 
         "desc": "列治文市，各类亚洲餐厅众多"},
    ],
    "shopping": [
        {"name": "南海岸广场", "lat": 33.6906, "lng": -117.8831, "type": "shopping", 
         "desc": "加州科斯塔梅萨，深受亚洲游客喜爱的高端购物中心"},
        {"name": "梅西百货(纽约)", "lat": 40.7505, "lng": -73.9934, "type": "shopping", 
         "desc": "纽约曼哈顿，支持Alipay支付，亚洲游客热门购物地"},
        {"name": "Nordstrom(旧金山)", "lat": 37.7879, "lng": -122.4075, "type": "shopping", 
         "desc": "旧金山联合广场，支持Alipay支付"},
        {"name": "Saks Fifth Avenue", "lat": 40.7614, "lng": -73.9776, "type": "shopping", 
         "desc": "纽约第五大道，支持Alipay支付，亚洲游客喜爱的奢侈品购物地"},
        {"name": "Tory Burch", "lat": 40.7614, "lng": -73.9776, "type": "shopping", 
         "desc": "纽约第五大道，支持Alipay支付"},
        {"name": "Kate Spade", "lat": 40.7614, "lng": -73.9776, "type": "shopping", 
         "desc": "纽约第五大道，支持Alipay支付"},
        {"name": "联合广场(旧金山)", "lat": 37.7879, "lng": -122.4075, "type": "shopping", 
         "desc": "旧金山购物中心，汇集众多高端品牌，亚洲游客热门购物地"},
        {"name": "第五大道(纽约)", "lat": 40.7614, "lng": -73.9776, "type": "shopping", 
         "desc": "纽约奢侈品购物街，众多品牌支持Alipay，亚洲游客必访"},
        {"name": "比佛利中心(洛杉矶)", "lat": 34.0736, "lng": -118.4004, "type": "shopping", 
         "desc": "洛杉矶比佛利山庄，高端购物中心，亚洲游客热门购物地"},
        {"name": "格罗夫购物中心(洛杉矶)", "lat": 34.0716, "lng": -118.3576, "type": "shopping", 
         "desc": "洛杉矶购物中心，汇集国际知名品牌，亚洲游客喜爱"},
        {"name": "伊顿中心(多伦多)", "lat": 43.6532, "lng": -79.3806, "type": "shopping", 
         "desc": "多伦多最大的购物中心，汇集众多国际品牌，亚洲游客热门购物地"},
        {"name": "太古广场(多伦多)", "lat": 43.8561, "lng": -79.3370, "type": "shopping", 
         "desc": "北美最大的亚洲购物中心之一，位于万锦市"},
        {"name": "时代坊(温哥华)", "lat": 49.1666, "lng": -123.1364, "type": "shopping", 
         "desc": "温哥华列治文市，提供丰富的亚洲商品"},
        {"name": "太平洋中心(温哥华)", "lat": 49.2794, "lng": -123.1189, "type": "shopping", 
         "desc": "温哥华主要购物中心，汇集众多国际品牌，亚洲游客热门购物地"},
        {"name": "拉斯维加斯大道", "lat": 36.1147, "lng": -115.1728, "type": "shopping", 
         "desc": "汇集众多奢侈品牌店和娱乐设施，亚洲游客喜爱的消费场所"},
        {"name": "奥特莱斯(洛杉矶)", "lat": 34.0522, "lng": -118.2437, "type": "shopping", 
         "desc": "洛杉矶奥特莱斯，亚洲游客喜爱的折扣购物地"},
        {"name": "奥特莱斯(纽约)", "lat": 40.7580, "lng": -73.9855, "type": "shopping", 
         "desc": "纽约奥特莱斯，亚洲游客喜爱的折扣购物地"},
    ],
    "tourism": [
        {"name": "金门大桥", "lat": 37.8199, "lng": -122.4783, "type": "tourism", 
         "desc": "旧金山标志性景点，每年吸引大量亚洲游客"},
        {"name": "自由女神像", "lat": 40.6892, "lng": -74.0445, "type": "tourism", 
         "desc": "纽约标志性景点，亚洲游客必访"},
        {"name": "时代广场", "lat": 40.7580, "lng": -73.9855, "type": "tourism", 
         "desc": "纽约著名景点，购物和娱乐中心，亚洲游客热门目的地"},
        {"name": "好莱坞星光大道", "lat": 34.1016, "lng": -118.3268, "type": "tourism", 
         "desc": "洛杉矶著名景点，亚洲游客必访"},
        {"name": "比佛利山庄", "lat": 34.0736, "lng": -118.4004, "type": "tourism", 
         "desc": "洛杉矶高端购物和旅游区，亚洲游客热门目的地"},
        {"name": "CN塔(多伦多)", "lat": 43.6426, "lng": -79.3871, "type": "tourism", 
         "desc": "多伦多标志性建筑，亚洲游客必访"},
        {"name": "斯坦利公园(温哥华)", "lat": 49.3000, "lng": -123.1417, "type": "tourism", 
         "desc": "温哥华著名景点，吸引大量亚洲游客"},
        {"name": "太空针塔(西雅图)", "lat": 47.6205, "lng": -122.3493, "type": "tourism", 
         "desc": "西雅图标志性建筑，亚洲游客必访"},
        {"name": "千禧公园(芝加哥)", "lat": 41.8825, "lng": -87.6244, "type": "tourism", 
         "desc": "芝加哥著名景点，吸引大量亚洲游客"},
        {"name": "哈佛大学", "lat": 42.3770, "lng": -71.1167, "type": "tourism", 
         "desc": "波士顿著名学府，吸引大量亚洲游客和学生"},
        {"name": "大峡谷", "lat": 36.1069, "lng": -112.1129, "type": "tourism", 
         "desc": "亚利桑那州，世界自然奇观，亚洲游客热门目的地"},
        {"name": "黄石国家公园", "lat": 44.4280, "lng": -110.5885, "type": "tourism", 
         "desc": "怀俄明州，世界著名国家公园，亚洲游客热门目的地"},
        {"name": "尼亚加拉大瀑布", "lat": 43.0962, "lng": -79.0377, "type": "tourism", 
         "desc": "美加边界，世界著名瀑布，亚洲游客热门目的地"},
    ],
    "alipay": [
        {"name": "Target(部分门店)", "lat": 40.7589, "lng": -73.8302, "type": "alipay", 
         "desc": "支持Alipay支付的大型零售商，亚洲游客常用"},
        {"name": "CVS Pharmacy(部分门店)", "lat": 40.7589, "lng": -73.8302, "type": "alipay", 
         "desc": "支持Alipay支付的连锁药店，亚洲游客常用"},
        {"name": "机场免税店", "lat": 40.6413, "lng": -73.7781, "type": "alipay", 
         "desc": "JFK、LAX、SFO等主要机场，支持Alipay支付，亚洲游客常用"},
        {"name": "7-Eleven(部分门店)", "lat": 34.0522, "lng": -118.2437, "type": "alipay", 
         "desc": "支持Alipay支付的便利店，亚洲游客常用"},
        {"name": "Walgreens(部分门店)", "lat": 40.7589, "lng": -73.8302, "type": "alipay", 
         "desc": "支持Alipay支付的连锁药店，亚洲游客常用"},
    ],
    "universities": [
        {"name": "哈佛大学", "lat": 42.3770, "lng": -71.1167, "type": "university", 
         "desc": "马萨诸塞州，大量亚洲留学生"},
        {"name": "MIT", "lat": 42.3601, "lng": -71.0942, "type": "university", 
         "desc": "马萨诸塞州，大量亚洲留学生"},
        {"name": "斯坦福大学", "lat": 37.4275, "lng": -122.1697, "type": "university", 
         "desc": "加州，大量亚洲留学生"},
        {"name": "UC Berkeley", "lat": 37.8719, "lng": -122.2585, "type": "university", 
         "desc": "加州，大量亚洲留学生"},
        {"name": "UCLA", "lat": 34.0689, "lng": -118.4452, "type": "university", 
         "desc": "加州，大量亚洲留学生"},
        {"name": "哥伦比亚大学", "lat": 40.8075, "lng": -73.9626, "type": "university", 
         "desc": "纽约，大量亚洲留学生"},
        {"name": "NYU", "lat": 40.7295, "lng": -73.9965, "type": "university", 
         "desc": "纽约，大量亚洲留学生"},
        {"name": "多伦多大学", "lat": 43.6532, "lng": -79.3832, "type": "university", 
         "desc": "多伦多，大量亚洲留学生"},
        {"name": "UBC", "lat": 49.2606, "lng": -123.2460, "type": "university", 
         "desc": "温哥华，大量亚洲留学生"},
        {"name": "USC", "lat": 34.0224, "lng": -118.2851, "type": "university", 
         "desc": "加州，大量亚洲留学生"},
        {"name": "UCSD", "lat": 32.8801, "lng": -117.2340, "type": "university", 
         "desc": "加州，大量亚洲留学生"},
    ]
}

def create_asia_map_with_plotly(return_fig=False):
    """创建全亚洲场景地图（不仅仅是华人，包括日韩、东南亚、南亚等）
    
    Args:
        return_fig: 如果为True，返回figure对象而不是保存文件
    
    Returns:
        如果return_fig=True，返回plotly figure对象；否则返回True/False表示是否成功
    """
    try:
        import plotly.graph_objects as go
        import plotly.express as px
        
        # 准备数据
        all_locations = []
        for category, items in asia_locations.items():
            for item in items:
                symbol = icon_symbols.get(item['type'], '📍')
                all_locations.append({
                    'name': item['name'],
                    'lat': item['lat'],
                    'lng': item['lng'],
                    'type': item['type'],
                    'desc': item['desc'],
                    'color': icon_colors[item['type']],
                    'symbol': symbol,
                    'type_name': icon_names[item['type']]
                })
        
        # 统计信息 - 按类型统计
        type_stats = {}
        for loc in all_locations:
            type_name = loc['type']
            type_stats[type_name] = type_stats.get(type_name, 0) + 1
        total_locations = len(all_locations)
        
        # 创建地图
        fig = go.Figure()
        
        # 按类型分组添加标记
        for type_name, color in icon_colors.items():
            type_locations = [loc for loc in all_locations if loc['type'] == type_name]
            if type_locations:
                size = marker_sizes.get(type_name, 10)
                symbol = icon_symbols.get(type_name, '📍')
                
                # 创建丰富的hover信息
                hover_texts = []
                for loc in type_locations:
                    hover_text = f"""
                    <b style='color: {color}; font-size: 16px;'>{loc['symbol']} {loc['name']}</b><br>
                    <span style='color: #666;'>类型：</span><b>{loc['type_name']}</b><br>
                    <span style='color: #666;'>{loc['desc']}</span><br>
                    <span style='color: #999; font-size: 11px;'>📍 {loc['lat']:.4f}, {loc['lng']:.4f}</span>
                    """
                    hover_texts.append(hover_text)
                
                fig.add_trace(go.Scattergeo(
                    lon=[loc['lng'] for loc in type_locations],
                    lat=[loc['lat'] for loc in type_locations],
                    text=[f"{loc['symbol']} {loc['name']}" for loc in type_locations],
                    mode='markers',
                    marker=dict(
                        size=size * 1.5,  # 放大标记以便更清晰
                        color=color,
                        line=dict(width=2.5, color='white'),
                        opacity=0.85
                    ),
                    name=f"{symbol} {icon_names[type_name]}",
                    hovertemplate='%{hovertext}<extra></extra>',
                    hovertext=hover_texts,
                    showlegend=True
                ))
        
        # 添加美国主要州名标注（使用州的地理中心坐标）
        us_states = [
            {"name": "CA", "lat": 36.7783, "lng": -119.4179},
            {"name": "NY", "lat": 42.1657, "lng": -74.9481},
            {"name": "TX", "lat": 31.0545, "lng": -97.5635},
            {"name": "FL", "lat": 27.7663, "lng": -81.6868},
            {"name": "IL", "lat": 40.3495, "lng": -88.9861},
            {"name": "MA", "lat": 42.2373, "lng": -71.5314},
            {"name": "WA", "lat": 47.0379, "lng": -120.5015},
            {"name": "PA", "lat": 40.5908, "lng": -77.2098},
            {"name": "HI", "lat": 21.3099, "lng": -157.8581},
            {"name": "NV", "lat": 38.3135, "lng": -117.0554},
            {"name": "AZ", "lat": 34.0489, "lng": -111.0937},
            {"name": "GA", "lat": 32.1656, "lng": -82.9001},
            {"name": "NC", "lat": 35.5397, "lng": -79.8431},
            {"name": "MI", "lat": 43.3266, "lng": -84.5361},
            {"name": "OH", "lat": 40.3888, "lng": -82.7649},
            {"name": "NJ", "lat": 40.2989, "lng": -74.5210},
            {"name": "VA", "lat": 37.7693, "lng": -78.1697},
            {"name": "OR", "lat": 43.8041, "lng": -120.5542},
            {"name": "CT", "lat": 41.5978, "lng": -72.7554},
            {"name": "CO", "lat": 39.0598, "lng": -105.3111},
        ]
        
        # 添加州名文本标注
        for state in us_states:
            fig.add_trace(go.Scattergeo(
                lon=[state['lng']],
                lat=[state['lat']],
                text=[state['name']],
                mode='text',
                textfont=dict(
                    size=10,
                    color='#666666',
                    family='Arial, sans-serif'
                ),
                showlegend=False,
                hoverinfo='skip'
            ))
        
        # 设置地图布局 - 使用更详细的地图样式
        fig.update_geos(
            projection_type="mercator",
            center=dict(lat=40, lon=-95),
            scope="north america",
            # 陆地、海洋、湖泊
            showland=True,
            landcolor="rgb(245, 245, 240)",  # 浅米色陆地，更自然
            showocean=True,
            oceancolor="rgb(230, 245, 255)",  # 浅蓝色海洋
            showlakes=True,
            lakecolor="rgb(200, 230, 255)",  # 浅蓝色湖泊
            showrivers=True,
            rivercolor="rgb(180, 220, 255)",  # 浅蓝色河流
            # 边界线
            coastlinecolor="rgb(80, 80, 80)",  # 深灰色海岸线
            coastlinewidth=1.5,
            showcountries=True,
            countrycolor="rgb(120, 120, 120)",  # 深灰色国家边界
            countrywidth=2,
            # 添加框架
            showframe=True,
            framecolor="rgb(100, 100, 100)",
            framewidth=1.5,
            # 分辨率设置（更详细）
            resolution=50  # 使用中等分辨率，显示更多细节
        )
        
        # 创建统计信息文本 - 使用类型名称，放大字体
        stats_text = f"<b style='font-size: 18px; color: #2c3e50;'>总地点数: {total_locations}</b><br><br>"
        for type_name in sorted(icon_colors.keys()):
            count = type_stats.get(type_name, 0)
            if count > 0:
                symbol = icon_symbols.get(type_name, '📍')
                stats_text += f"<span style='font-size: 15px;'>{symbol} {icon_names[type_name]}: {count}</span><br>"
        
        fig.update_layout(
            height=900,
            geo=dict(
                lonaxis_range=[-170, -50],
                lataxis_range=[15, 70],
                bgcolor='rgba(0,0,0,0)'
            ),
            legend=dict(
                yanchor="top",
                y=0.95,
                xanchor="left",
                x=0.005,  # 往左移动（从0.02减小到0.015，约5px的偏移）
                bgcolor="rgba(255, 255, 255, 0.92)",
                bordercolor="rgba(0, 0, 0, 0.3)",
                borderwidth=2,
                font=dict(size=15, family='Microsoft YaHei, Arial, sans-serif'),  # 放大字体
                itemclick="toggleothers",
                itemdoubleclick="toggle",
                title=dict(
                    text="<b style='font-size: 18px;'>图例</b>",
                    font=dict(size=18, color='#2c3e50')
                )
            ),
            paper_bgcolor='white',
            plot_bgcolor='white',
            margin=dict(l=0, r=0, t=0, b=0)
        )
        
        # 添加标题注释 - 直接嵌入到地图画布中
        fig.add_annotation(
            text="<b style='font-size: 22px; color: #2c3e50;'>🌏 全亚洲游客/居民消费场景地图</b>",
            xref="paper", yref="paper",
            x=0.5, y=0.98,
            xanchor="center", yanchor="top",
            bgcolor="rgba(255, 255, 255, 0.92)",
            bordercolor="rgba(0, 0, 0, 0.3)",
            borderwidth=2,
            borderpad=12,
            font=dict(size=18, family='Microsoft YaHei, Arial, sans-serif', color='#2c3e50'),
            showarrow=False,
            align="center"
        )
        
        # 添加统计信息注释 - 移到左侧，放在图例下方
        fig.add_annotation(
            text=stats_text,
            xref="paper", yref="paper",
            x=0.005, y=0.65,  # 往左移动，与图例对齐（从0.02减小到0.015）
            xanchor="left", yanchor="top",
            bgcolor="rgba(255, 255, 255, 0.92)",
            bordercolor="rgba(0, 0, 0, 0.3)",
            borderwidth=2,
            borderpad=12,
            font=dict(size=14, family='Microsoft YaHei, Arial, sans-serif', color='#2c3e50'),  # 放大字体
            showarrow=False,
            align="left"
        )
        
        # 如果只需要返回figure对象（用于Streamlit等），直接返回
        if return_fig:
            return fig
        
        # 否则保存地图文件
        output_file = 'north_america_asia_communities_map_plotly.html'
        fig.write_html(output_file, config={'displayModeBar': True, 'displaylogo': False})
        print(f"✅ Plotly地图已保存: {output_file}")
        return True
        
    except ImportError:
        if return_fig:
            return None
        print("❌ plotly未安装，尝试安装: pip install plotly")
        return False

def create_map_with_matplotlib():
    """使用matplotlib创建静态地图"""
    try:
        import matplotlib.pyplot as plt
        import cartopy.crs as ccrs
        import cartopy.feature as cfeature
        
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 创建图形和地图
        fig = plt.figure(figsize=(18, 12))
        ax = plt.axes(projection=ccrs.PlateCarree())
        
        # 设置地图范围
        ax.set_extent([-170, -50, 15, 70], crs=ccrs.PlateCarree())
        
        # 添加地图特征 - 使用更柔和的颜色
        ax.add_feature(cfeature.COASTLINE, linewidth=0.8, color='#666666')
        ax.add_feature(cfeature.BORDERS, linewidth=0.6, color='#888888', linestyle='--')
        ax.add_feature(cfeature.LAND, color='#f0f8ff', edgecolor='#cccccc')
        ax.add_feature(cfeature.OCEAN, color='#e0f2f7')
        ax.add_feature(cfeature.LAKES, color='#b0e0e6', edgecolor='#87CEEB')
        
        # 统计信息 - 按类型统计
        type_stats = {}
        for category, items in locations.items():
            for item in items:
                type_name = item['type']
                type_stats[type_name] = type_stats.get(type_name, 0) + 1
        total_locations = sum(type_stats.values())
        
        # 按类型分组添加标记，避免重复图例
        plotted_types = set()
        for category, items in locations.items():
            for item in items:
                color = icon_colors.get(item['type'], '#666666')
                size = marker_sizes.get(item['type'], 10)
                type_name = item['type']
                
                # 只在第一次绘制该类型时添加图例标签
                label = None
                if type_name not in plotted_types:
                    label = f"{icon_symbols.get(type_name, '📍')} {icon_names[type_name]}"
                    plotted_types.add(type_name)
                
                ax.plot(
                    item['lng'], item['lat'],
                    marker='o',
                    markersize=size,
                    color=color,
                    markeredgecolor='white',
                    markeredgewidth=2.5,
                    transform=ccrs.PlateCarree(),
                    label=label,
                    alpha=0.85,
                    zorder=10
                )
        
        # 添加标题
        plt.title('🗺️ 北美华人社区、商家与旅游场景地图', 
                 fontsize=20, fontweight='bold', pad=25, color='#2c3e50')
        
        # 添加美化的图例
        legend = ax.legend(
            loc='upper left',
            bbox_to_anchor=(0.02, 0.98),
            fontsize=11,
            frameon=True,
            fancybox=True,
            shadow=True,
            framealpha=0.95,
            edgecolor='#cccccc',
            borderpad=1,
            labelspacing=1.2
        )
        legend.get_frame().set_facecolor('white')
        
        # 添加统计信息文本框 - 使用类型名称
        stats_text = f"总地点数: {total_locations}\n"
        for type_name in sorted(icon_colors.keys(), key=lambda x: type_stats.get(x, 0), reverse=True):
            count = type_stats.get(type_name, 0)
            if count > 0:
                symbol = icon_symbols.get(type_name, '📍')
                stats_text += f"{symbol} {icon_names[type_name]}: {count}\n"
        
        # 在右下角添加统计信息
        textstr = stats_text.strip()
        props = dict(boxstyle='round,pad=1', facecolor='white', edgecolor='#cccccc', 
                    alpha=0.95, linewidth=1.5)
        ax.text(0.98, 0.02, textstr, transform=ax.transAxes, fontsize=10,
               verticalalignment='bottom', horizontalalignment='right',
               bbox=props, family='monospace')
        
        # 添加网格线（可选）
        ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', 
                    alpha=0.3, linestyle='--', zorder=5)
        
        # 保存地图
        output_file = 'north_america_chinese_communities_map_matplotlib.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
        print(f"✅ Matplotlib地图已保存: {output_file}")
        plt.close()
        return True
        
    except ImportError:
        print("❌ matplotlib/cartopy未安装，尝试安装: pip install matplotlib cartopy")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("北美华人社区、商家与旅游场景地图生成器")
    print("=" * 60)
    print()
    
    # 尝试使用不同的库
    success = False
    
    # 1. 尝试使用plotly（推荐，国内可访问）
    print("📊 尝试使用 Plotly 创建地图...")
    if create_map_with_plotly():
        success = True
        print("✅ Plotly地图创建成功！")
    else:
        print("⚠️  Plotly不可用，尝试其他方法...")
    
    print()
    
    # 2. 尝试使用folium
    print("📊 尝试使用 Folium 创建地图...")
    if create_map_with_folium():
        success = True
        print("✅ Folium地图创建成功！")
    else:
        print("⚠️  Folium不可用，尝试其他方法...")
    
    print()
    
    # 3. 尝试使用matplotlib（静态地图）
    print("📊 尝试使用 Matplotlib 创建静态地图...")
    if create_map_with_matplotlib():
        success = True
        print("✅ Matplotlib地图创建成功！")
    else:
        print("⚠️  Matplotlib不可用")
    
    print()
    
    if success:
        print("=" * 60)
        print("✅ 地图生成完成！")
        print("=" * 60)
        print("\n生成的文件：")
        if os.path.exists('north_america_chinese_communities_map_plotly.html'):
            print("  - north_america_chinese_communities_map_plotly.html (推荐)")
        if os.path.exists('north_america_chinese_communities_map_folium.html'):
            print("  - north_america_chinese_communities_map_folium.html")
        if os.path.exists('north_america_chinese_communities_map_matplotlib.png'):
            print("  - north_america_chinese_communities_map_matplotlib.png")
    else:
        print("=" * 60)
        print("❌ 无法创建地图，请安装必要的库：")
        print("   pip install plotly folium matplotlib cartopy")
        print("=" * 60)

if __name__ == "__main__":
    main()
