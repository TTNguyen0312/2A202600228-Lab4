from langchain_core.tools import tool

FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1_450_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2_800_000, "class": "business"},
        {"airline": "VietJet Air",      "departure": "08:30", "arrival": "09:50", "price": 890_000,   "class": "economy"},
        {"airline": "Bamboo Airways",   "departure": "11:00", "arrival": "12:20", "price": 1_200_000, "class": "economy"},
    ],
    ("Đà Nẵng", "Hà Nội"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1_450_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2_800_000, "class": "business"},
        {"airline": "VietJet Air",      "departure": "08:30", "arrival": "09:50", "price": 890_000,   "class": "economy"},
        {"airline": "Bamboo Airways",   "departure": "11:00", "arrival": "12:20", "price": 1_200_000, "class": "economy"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2_100_000, "class": "economy"},
        {"airline": "VietJet Air",      "departure": "10:00", "arrival": "12:15", "price": 1_350_000, "class": "economy"},
        {"airline": "VietJet Air",      "departure": "16:00", "arrival": "18:15", "price": 1_100_000, "class": "economy"},
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1_600_000, "class": "economy"},
        {"airline": "VietJet Air",      "departure": "07:30", "arrival": "09:40", "price": 950_000,   "class": "economy"},
        {"airline": "Bamboo Airways",   "departure": "12:00", "arrival": "14:10", "price": 1_300_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3_200_000, "class": "business"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1_300_000, "class": "economy"},
        {"airline": "VietJet Air",      "departure": "13:00", "arrival": "14:20", "price": 780_000,   "class": "economy"},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1_100_000, "class": "economy"},
        {"airline": "VietJet Air",      "departure": "15:00", "arrival": "16:00", "price": 650_000,   "class": "economy"},
    ],
}

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury",    "stars": 5, "price_per_night": 1_800_000, "area": "Mỹ Khê",    "rating": 4.5},
        {"name": "Sala Danang Beach",     "stars": 4, "price_per_night": 1_200_000, "area": "Mỹ Khê",    "rating": 4.3},
        {"name": "Fivitel Danang",        "stars": 3, "price_per_night": 650_000,   "area": "Sơn Trà",   "rating": 4.1},
        {"name": "Memory Hostel",         "stars": 2, "price_per_night": 250_000,   "area": "Hải Châu",  "rating": 4.6},
        {"name": "Christina's Homestay", "stars": 2, "price_per_night": 350_000,   "area": "An Thượng",  "rating": 4.7},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort",  "stars": 5, "price_per_night": 3_500_000, "area": "Bãi Dài",    "rating": 4.4},
        {"name": "Sol by Meliá",     "stars": 4, "price_per_night": 1_500_000, "area": "Bãi Trường", "rating": 4.2},
        {"name": "Lahana Resort",    "stars": 3, "price_per_night": 800_000,   "area": "Dương Đông", "rating": 4.0},
        {"name": "9Station Hostel",  "stars": 2, "price_per_night": 200_000,   "area": "Dương Đông", "rating": 4.5},
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel",        "stars": 5, "price_per_night": 2_800_000, "area": "Quận 1", "rating": 4.3},
        {"name": "Liberty Central",  "stars": 4, "price_per_night": 1_400_000, "area": "Quận 1", "rating": 4.1},
        {"name": "Cochin Zen Hotel", "stars": 3, "price_per_night": 550_000,   "area": "Quận 3", "rating": 4.4},
        {"name": "The Common Room",  "stars": 2, "price_per_night": 180_000,   "area": "Quận 1", "rating": 4.6},
    ],
}


@tool
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm các chuyến bay giữa hai thành phố.
    Tham số:
    - origin: thành phố khởi hành (VD: 'Hà Nội', 'Hồ Chí Minh')
    - destination: thành phố đến (VD: 'Đà Nẵng', 'Phú Quốc')
    Trả về danh sách chuyến bay với hãng, giờ bay, giá vé.
    Nếu không tìm thấy tuyến bay, trả về thông báo không có chuyến.
    """
    def fmt_price(p):
        return f"{p:,}đ".replace(",", ".")

    try:
        # Hỗ trợ tìm kiếm ngược nếu không có chuyến bay theo hướng origin → destination
        flights = FLIGHTS_DB.get((origin, destination))
        reversed_search = False
        if flights is None:
            flights = FLIGHTS_DB.get((destination, origin))
            reversed_search = True

        if not flights:
            return f"Không tìm thấy chuyến bay từ {origin} đến {destination}."

        if reversed_search:
            lines = [f"Không tìm thấy chuyến bay từ {origin} đến {destination}. Tuy nhiên, có các chuyến bay ngược lại:"]
            origin, destination = destination, origin
        else:
            lines = [f"Chuyến bay từ {origin} đến {destination}:"]

        # Format giá tiền và xuất kết quả
        for i, f in enumerate(flights, 1):
            lines.append(
                f"  {i}. {f['airline']} | {f['departure']} → {f['arrival']} "
                f"| {fmt_price(f['price'])} | {f['class']}"
            )
        return "\n".join(lines)
    except Exception as e:
        return f"Lỗi khi tìm chuyến bay: {e}"


@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm.
    Tham số:
    - city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
    - max_price_per_night: giá tối đa mỗi đêm (VNĐ), mặc định không giới hạn
    Trả về danh sách khách sạn phù hợp với tên, số sao, giá, khu vực, rating.
    """
    def fmt_price(p):
        return f"{p:,}đ".replace(",", ".")

    try:
        # Tìm hotel by city, lọc theo giá, sắp xếp theo rating giảm dần
        hotels = HOTELS_DB.get(city, [])
        filtered = [h for h in hotels if h["price_per_night"] <= max_price_per_night]
        filtered.sort(key=lambda h: h["rating"], reverse=True)

        if not filtered:
            return (
                f"Không tìm thấy khách sạn tại {city} với giá dưới "
                f"{fmt_price(max_price_per_night)}/đêm. Hãy thử tăng ngân sách."
            )

        # Format kết quả
        lines = [f"Khách sạn tại {city}:"]
        for i, h in enumerate(filtered, 1):
            stars = "★" * h["stars"]
            lines.append(
                f"  {i}. {h['name']} {stars} | {fmt_price(h['price_per_night'])}/đêm "
                f"| {h['area']} | Rating: {h['rating']}"
            )
        return "\n".join(lines)
    except Exception as e:
        return f"Lỗi khi tìm khách sạn: {e}"


@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.
    Tham số:
    - total_budget: tổng ngân sách ban đầu (VNĐ)
    - expenses: chuỗi mô tả các khoản chi, mỗi khoản cách nhau bởi dấu phẩy,
      định dạng 'tên_khoản:số_tiền' (VD: 've_may_bay:890000,khach_san:650000')
    Trả về bảng chi tiết các khoản chi và số tiền còn lại.
    Nếu vượt ngân sách, cảnh báo rõ ràng số tiền thiếu.
    """
    def fmt_price(p):
        return f"{p:,}đ".replace(",", ".")

    try:
        # Parse expenses string vào dict
        parsed = {}
        for item in expenses.split(","):
            item = item.strip()
            if not item:
                continue
            if ":" not in item:
                return f"Lỗi: mục '{item}' thiếu dấu ':'. Dùng định dạng 'tên:số_tiền'."
            name, amount = item.rsplit(":", 1)
            parsed[name.strip()] = int(amount.strip())

        # Tính tổng chi và số tiền còn lại
        total_spent = sum(parsed.values())
        remaining = total_budget - total_spent

        # Format kết quả
        lines = ["Bảng chi phí:"]
        for name, amount in parsed.items():
            lines.append(f"  - {name}: {fmt_price(amount)}")
        lines.append("  ---")
        lines.append(f"Tổng chi:  {fmt_price(total_spent)}")
        lines.append(f"Ngân sách: {fmt_price(total_budget)}")

        if remaining >= 0:
            lines.append(f"Còn lại:   {fmt_price(remaining)}")
        else:
            lines.append(f"Còn lại:   -{fmt_price(abs(remaining))}")
            lines.append(f"⚠️ Vượt ngân sách {fmt_price(abs(remaining))}! Cần điều chỉnh.")

        return "\n".join(lines)
    except ValueError:
        return "Lỗi: số tiền không hợp lệ. Vui lòng dùng số nguyên (VD: 've_may_bay:890000')."
    except Exception as e:
        return f"Lỗi khi tính ngân sách: {e}"

# Database cho use case bổ sung: danh sách địa điểm tham quan tại các thành phố, với thông tin tên, loại hình, thời gian tham quan, chi phí vào cửa, khu vực. Đây sẽ là dữ liệu cho tool get_attractions.
ATTRACTIONS_DB = {
    "Đà Nẵng": [
        {"name": "Bà Nà Hills",          "type": "theme_park",    "duration_hours": 6, "cost": 750_000, "area": "Tây Đà Nẵng"},
        {"name": "Cầu Vàng",             "type": "landmark",      "duration_hours": 1, "cost": 0,       "area": "Bà Nà Hills"},
        {"name": "Bãi biển Mỹ Khê",      "type": "beach",         "duration_hours": 3, "cost": 0,       "area": "Mỹ Khê"},
        {"name": "Ngũ Hành Sơn",         "type": "nature",        "duration_hours": 2, "cost": 40_000,  "area": "Non Nước"},
        {"name": "Phố cổ Hội An",        "type": "heritage",      "duration_hours": 4, "cost": 120_000, "area": "Hội An (cách 30km)"},
        {"name": "Bảo tàng Chăm",        "type": "museum",        "duration_hours": 2, "cost": 60_000,  "area": "Hải Châu"},
        {"name": "Chợ Hàn",              "type": "market",        "duration_hours": 1, "cost": 0,       "area": "Hải Châu"},
        {"name": "Bán đảo Sơn Trà",      "type": "nature",        "duration_hours": 3, "cost": 0,       "area": "Sơn Trà"},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Safari",       "type": "zoo",           "duration_hours": 4, "cost": 600_000, "area": "Bắc Đảo"},
        {"name": "Grand World",           "type": "entertainment", "duration_hours": 4, "cost": 300_000, "area": "Bắc Đảo"},
        {"name": "Bãi Sao",              "type": "beach",         "duration_hours": 3, "cost": 0,       "area": "Nam Đảo"},
        {"name": "Làng chài Hàm Ninh",   "type": "culture",       "duration_hours": 2, "cost": 0,       "area": "Đông Đảo"},
        {"name": "Cáp treo Hòn Thơm",    "type": "landmark",      "duration_hours": 3, "cost": 450_000, "area": "Nam Đảo"},
        {"name": "Chợ đêm Phú Quốc",     "type": "market",        "duration_hours": 2, "cost": 0,       "area": "Dương Đông"},
        {"name": "Rừng nguyên sinh",      "type": "nature",        "duration_hours": 3, "cost": 0,       "area": "Trung Đảo"},
        {"name": "Bãi Dài",              "type": "beach",         "duration_hours": 3, "cost": 0,       "area": "Bắc Đảo"},
    ],
    "Hồ Chí Minh": [
        {"name": "Dinh Độc Lập",          "type": "heritage",      "duration_hours": 2, "cost": 40_000,  "area": "Quận 1"},
        {"name": "Bảo tàng Chiến tranh",  "type": "museum",        "duration_hours": 2, "cost": 60_000,  "area": "Quận 3"},
        {"name": "Chợ Bến Thành",         "type": "market",        "duration_hours": 2, "cost": 0,       "area": "Quận 1"},
        {"name": "Phố đi bộ Nguyễn Huệ", "type": "landmark",      "duration_hours": 1, "cost": 0,       "area": "Quận 1"},
        {"name": "Địa đạo Củ Chi",        "type": "heritage",      "duration_hours": 5, "cost": 110_000, "area": "Củ Chi (cách 70km)"},
        {"name": "Bưu điện Trung tâm",    "type": "landmark",      "duration_hours": 1, "cost": 0,       "area": "Quận 1"},
        {"name": "Chùa Jade Emperor",     "type": "culture",       "duration_hours": 1, "cost": 0,       "area": "Quận 3"},
        {"name": "Khu Phố Tây Bùi Viện", "type": "entertainment", "duration_hours": 3, "cost": 0,       "area": "Quận 1"},
    ],
    "Hà Nội": [
        {"name": "Hồ Hoàn Kiếm",          "type": "landmark",      "duration_hours": 1, "cost": 0,       "area": "Hoàn Kiếm"},
        {"name": "Văn Miếu",              "type": "heritage",      "duration_hours": 2, "cost": 30_000,  "area": "Đống Đa"},
        {"name": "Lăng Bác Hồ",          "type": "heritage",      "duration_hours": 2, "cost": 0,       "area": "Ba Đình"},
        {"name": "Phố cổ Hà Nội",         "type": "culture",       "duration_hours": 3, "cost": 0,       "area": "Hoàn Kiếm"},
        {"name": "Bảo tàng Dân tộc học",  "type": "museum",        "duration_hours": 2, "cost": 40_000,  "area": "Cầu Giấy"},
        {"name": "Chùa Trấn Quốc",        "type": "culture",       "duration_hours": 1, "cost": 0,       "area": "Tây Hồ"},
        {"name": "Chợ Đồng Xuân",         "type": "market",        "duration_hours": 2, "cost": 0,       "area": "Hoàn Kiếm"},
        {"name": "Nhà hát Lớn",           "type": "landmark",      "duration_hours": 1, "cost": 0,       "area": "Hoàn Kiếm"},
    ],
}

# Tool cho use case bổ sung: Lấy danh sách địa điểm tham quan tại một thành phố, với thông tin tên, loại hình, thời gian tham quan, chi phí vào cửa, khu vực. Đây sẽ là tool get_attractions mà specialist node tour_guide sẽ gọi đến khi cần gợi ý địa điểm tham quan.
@tool
def get_attractions(city: str) -> str:
    """
    Lấy danh sách địa điểm tham quan tại một thành phố.
    Tham số:
    - city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh', 'Hà Nội')
    Trả về danh sách địa điểm với tên, loại hình, thời gian tham quan, chi phí vào cửa, khu vực.
    """
    def fmt_price(p):
        return "Miễn phí" if p == 0 else f"{p:,}đ".replace(",", ".")

    try:
        # Tìm attractions by city
        attractions = ATTRACTIONS_DB.get(city)
        if not attractions:
            return f"Không có dữ liệu địa điểm tham quan cho {city}."

        # Format kết quả
        lines = [f"Địa điểm tham quan tại {city}:"]
        for i, a in enumerate(attractions, 1):
            lines.append(
                f"  {i}. {a['name']} [{a['type']}] | ~{a['duration_hours']}h "
                f"| Vào cửa: {fmt_price(a['cost'])} | {a['area']}"
            )
        return "\n".join(lines)
    except Exception as e:
        return f"Lỗi khi lấy địa điểm tham quan: {e}"
