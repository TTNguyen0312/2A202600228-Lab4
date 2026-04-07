**Test Case 1**:
Bạn: Xin chào tôi muốn đi du lịch nhưng chưa biết đi đâu

TravelBuddy đang suy nghĩ...
  [classifier] intent = tour_guide
  [tour_guide] direct reply

TravelBuddy: Chào bạn! Để giúp bạn chọn điểm đến phù hợp, bạn có thể cho mình biết sở thích của bạn không? Dưới đây là một số gợi ý dựa trên sở thích:

- Nếu bạn thích núi và khí hậu lạnh, bạn có thể xem xét Đà Lạt, Sa Pa, hoặc Mù Cang Chải.
- Nếu bạn thích biển, Đà Nẵng, Phú Quốc, hoặc Nha Trang là những lựa chọn tuyệt vời.
- Nếu bạn yêu thích văn hóa và phố cổ, hãy cân nhắc Hà Nội, Hội An, hoặc Huế.
- Nếu bạn thích những thành phố náo nhiệt, Hồ Chí Minh và Hà Nội sẽ rất phù hợp.

Bạn thích loại trải nghiệm nào nhất?

Bạn: Núi, khí hậu lạnh

TravelBuddy đang suy nghĩ...
  [classifier] intent = tour_guide
  [tour_guide] direct reply

TravelBuddy: Bạn thích khám phá núi và tận hưởng không khí lạnh? Tôi đề xuất một số địa điểm tuyệt vời cho bạn: Đà Lạt, Sa Pa, và Mù Cang Chải. Bạn muốn tìm hiểu thêm về địa điểm nào để tôi có thể lên lịch trình tham quan cho bạn?

Bạn: Đà Lạt có gì hay

TravelBuddy đang suy nghĩ...
  [classifier] intent = tour_guide
  [tour_guide] tool call → get_attractions({'city': 'Đà Lạt'})
  [tour_guide] direct reply

TravelBuddy: Hiện tại, mình không có dữ liệu cụ thể về các địa điểm tham quan tại Đà Lạt. Tuy nhiên, mình có thể chia sẻ với bạn một số trải nghiệm thú vị ở Đà Lạt mà nhiều người thường thích:

1. **Hồ Xuân Hương**: Một hồ nước lớn nằm ngay trung tâm thành phố, xung quanh là công viên cây xanh, thích hợp để đi dạo hoặc đạp xe.

2. **Thung Lũng Tình Yêu**: Nơi có cảnh quan thơ mộng với nhiều hoa và cây xanh, là điểm đến lý tưởng cho các cặp đôi.

3. **Nhà thờ Domaine de Marie**: Một công trình kiến trúc Pháp tuyệt đẹp, rất đáng để ghé thăm.

4. **Chợ Đà Lạt**: Nơi bạn có thể thưởng thức các món ăn đặc sản và mua sắm đồ lưu niệm.

5. **Vườn hoa Đà Lạt**: Rực rỡ với hàng ngàn loài hoa khác nhau, là điểm đến không thể bỏ qua cho những ai yêu thích thiên nhiên.

6. **Cáp treo Đà Lạt**: Trải nghiệm cảm giác lơ lửng trên không và ngắm nhìn toàn cảnh thành phố từ trên cao.

Nếu bạn muốn có lịch trình chi tiết hoặc cần thêm gợi ý, hãy cho mình biết nhé!

Bạn: Tôi ở Hà Nội, muốn đi Đà Lạt 3 ngày, budget tầm 4,000,000 VND, lên kế hoạch cho tôi nhé

TravelBuddy đang suy nghĩ...
  [classifier] intent = trip_planner
  [trip_planner] tool call → search_flights({'origin': 'Hà Nội', 'destination': 'Đà Lạt'})
  [trip_planner] tool call → search_hotels({'city': 'Đà Lạt', 'max_price_per_night': 1000000})
  [trip_planner] direct reply

TravelBuddy: Mình không tìm thấy chuyến bay từ Hà Nội đến Đà Lạt và cũng không có khách sạn tại Đà Lạt với giá dưới 1.000.000đ/đêm. 

Có thể bạn muốn thử tăng ngân sách hoặc xem xét thay đổi điểm đến? Nếu có bất kỳ yêu cầu nào khác, hãy cho mình biết nhé!

Bạn: Thế lên kế hoạch đi Đà Nẵng với thời gian và ngân sách tương tự 

TravelBuddy đang suy nghĩ...
  [classifier] intent = trip_planner
  [trip_planner] tool call → search_flights({'origin': 'Hà Nội', 'destination': 'Đà Nẵng'})
  [trip_planner] tool call → search_hotels({'city': 'Đà Nẵng', 'max_price_per_night': 1000000})
  [trip_planner] tool call → calculate_budget({'total_budget': 5000000, 'expenses': 've_may_bay:890000,khach_san:750000'})
  [trip_planner] direct reply

TravelBuddy: Chuyến bay: 
1. VietJet Air | 08:30 → 09:50 | 890.000đ | economy

Khách sạn: 
1. Memory Hostel ★★ | 250.000đ/đêm | Hải Châu | Rating: 4.6 (3 đêm = 750.000đ)

Tổng chi phí ước tính: 1.640.000đ (bao gồm vé máy bay và 3 đêm khách sạn).

Gợi ý thêm: Bạn còn dư ~3.360.000đ để ăn uống và tham quan Bà Nà Hills, Hội An!


**Test Case 2**:
Bạn: Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng

TravelBuddy đang suy nghĩ...
  [classifier] intent = trip_planner
  [trip_planner] tool call → search_flights({'origin': 'Hà Nội', 'destination': 'Đà Nẵng'})
  [trip_planner] direct reply

TravelBuddy: Dưới đây là một số chuyến bay từ Hà Nội đi Đà Nẵng:

1. **Vietnam Airlines** | 06:00 → 07:20 | 1.450.000đ | economy
2. **Vietnam Airlines** | 14:00 → 15:20 | 2.800.000đ | business
3. **VietJet Air** | 08:30 → 09:50 | 890.000đ | economy
4. **Bamboo Airways** | 11:00 → 12:20 | 1.200.000đ | economy

Bạn cần thêm thông tin gì nữa không?

**Test Case 3**:
Bạn: Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!

TravelBuddy đang suy nghĩ...
  [classifier] intent = trip_planner
  [trip_planner] tool call → search_flights({'origin': 'Hà Nội', 'destination': 'Phú Quốc'})
  [trip_planner] tool call → search_hotels({'city': 'Phú Quốc', 'max_price_per_night': 2500000})
  [trip_planner] tool call → calculate_budget({'total_budget': 5000000, 'expenses': 've_may_bay:1350000,khach_san:400000'})
  [trip_planner] direct reply

TravelBuddy: Dưới đây là thông tin chuyến đi của bạn từ Hà Nội đến Phú Quốc:

**Chuyến bay:**
1. VietJet Air | 10:00 → 12:15 | 1.350.000đ | economy

**Khách sạn:**
- **9Station Hostel ★★** | 200.000đ/đêm | Dương Đông | Rating: 4.5 (2 đêm x 200.000đ = 400.000đ)
  
**Tổng chi phí ước tính:**
- Vé máy bay: 1.350.000đ
- Khách sạn: 400.000đ
- **Tổng chi:** 1.750.000đ

**Ngân sách: 5.000.000đ**
- **Còn lại:** 3.250.000đ

**Gợi ý thêm:** Bạn còn dư khá nhiều ngân sách để thưởng thức hải sản, tham quan các điểm du lịch nổi tiếng, hay thậm chí tham gia các hoạt động như lặn biển hay đi tour khám phá đảo!

Chúc bạn có một chuyến đi vui vẻ! Nếu cần thêm thông tin gì, cứ hỏi mình nhé!

**Test Case 4**:
Bạn: Tôi muốn đặt khách sạn

TravelBuddy đang suy nghĩ...
  [classifier] intent = trip_planner
  [trip_planner] direct reply

TravelBuddy: Tôi không có đủ thông tin. Bạn có thể cho tôi biết thành phố bạn muốn đặt khách sạn và ngân sách mỗi đêm không?

Bạn: Phú Quốc, mỗi đêm dưới 500,000

TravelBuddy đang suy nghĩ...
  [classifier] intent = trip_planner
  [trip_planner] tool call → search_hotels({'city': 'Phú Quốc', 'max_price_per_night': 500000})
  [trip_planner] direct reply

TravelBuddy: Khách sạn tại Phú Quốc mà mình tìm thấy là:

- **9Station Hostel ★★** | 200.000đ/đêm | Dương Đông | Rating: 4.5

Nếu bạn cần thêm thông tin hoặc lên kế hoạch cho chuyến đi, hãy cho mình biết nhé!

**Test Case 5**:
Bạn: Giải giúp tôi bài tập lập trình Python về Linked List

TravelBuddy đang suy nghĩ...
  [classifier] intent = off_topic

TravelBuddy: Mình chỉ có thể hỗ trợ về du lịch thôi bạn nhé! Bạn muốn tìm vé/khách sạn hay lên lịch trình tham quan?

**Test Case 6**: 
Bạn: Đà Nẵng có những địa điểm nào

TravelBuddy đang suy nghĩ...
  [classifier] intent = tour_guide
  [tour_guide] tool call → get_attractions({'city': 'Đà Nẵng'})
  [tour_guide] direct reply

TravelBuddy: Tuyệt vời, Đà Nẵng có rất nhiều địa điểm thú vị để khám phá. Dưới đây là gợi ý lịch trình tham quan trong 2 ngày:

🗓 Ngày 1 – "Khám phá thiên nhiên và di sản"
  🌅 Sáng: Bà Nà Hills (~6h) – 750.000đ – Khám phá khu vui chơi giải trí trên núi với nhiều hoạt động thú vị và cảnh quan đẹp như mơ.
  ☀️ Chiều: Cầu Vàng (~1h) – Miễn phí – Chiêm ngưỡng cây cầu nổi tiếng với kiến trúc đặc biệt nằm trong khu vực Bà Nà Hills.
  🌙 Tối: Thưởng thức các món ăn hải sản tươi ngon tại các nhà hàng dọc bãi biển Mỹ Khê.

Gợi ý thêm: Nếu bạn thích đi bộ, hãy mang giày thể thao thoải mái vì Bà Nà Hills có nhiều điểm tham quan nằm rải rác.

🗓 Ngày 2 – "Biển và văn hóa"
  🌅 Sáng: Bãi biển Mỹ Khê (~3h) – Miễn phí – Thư giãn và tắm biển tại một trong những bãi biển đẹp nhất Việt Nam.
  ☀️ Chiều: Ngũ Hành Sơn (~2h) – 40.000đ – Khám phá các hang động và chùa chiền nằm trong quần thể núi đá vôi nổi tiếng.
  🌙 Tối: Tham quan phố cổ Hội An (~4h) – 120.000đ – Dạo bước trong không gian cổ kính, thưởng thức đặc sản Hội An như cao lầu, bánh mì Phượng.

Gợi ý thêm: Hội An cách Đà Nẵng khoảng 30km, bạn có thể thuê xe máy hoặc taxi để di chuyển. Thời gian di chuyển khoảng 45 phút.

Hy vọng lịch trình trên sẽ mang lại cho bạn những trải nghiệm tuyệt vời tại Đà Nẵng!