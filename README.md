# Hệ Thống Phân loại và Đếm tiền
Dưới đây là mẫu báo cáo GitHub/README.md cho đề tài:

Hệ Thống Phân Loại Và Đếm Tiền Sử Dụng ORB + Homography

## Giới thiệu

Đề tài xây dựng hệ thống nhận dạng và đếm tiền Việt Nam từ ảnh chụp các tờ tiền nằm rải rác trên mặt bàn bằng kỹ thuật xử lý ảnh.

Đầu vào

Ảnh chứa một hoặc nhiều tờ tiền Việt Nam.

Các tờ tiền có thể khác mệnh giá, xoay góc hoặc thay đổi kích thước.


Đầu ra

Bounding Box bao quanh từng tờ tiền.

Nhận dạng mệnh giá từng tờ tiền.

Thống kê số lượng từng loại tiền.

Tính tổng số tiền trong ảnh.



---

## Mục tiêu

Xây dựng chương trình có khả năng:

Phát hiện vị trí các tờ tiền.

Nhận dạng mệnh giá bằng đặc trưng ảnh.

Hoạt động không cần huấn luyện mô hình AI.

Tính tổng giá trị tiền trong ảnh.



---

## Công nghệ sử dụng

OpenCV

Thư viện xử lý ảnh dùng để:

Đọc ảnh

Tiền xử lý

Trích xuất đặc trưng

Vẽ Bounding Box


ORB (Oriented FAST and Rotated BRIEF)

ORB là thuật toán phát hiện và mô tả đặc trưng ảnh.

Ưu điểm:

Miễn phí

Tốc độ nhanh

Chống xoay tốt

Không cần huấn luyện


Homography

Homography được sử dụng để:

Xác định phép biến đổi giữa ảnh mẫu và ảnh cần nhận dạng.

Tìm chính xác vị trí của tờ tiền trong ảnh.

Vẽ Bounding Box theo góc xoay thực tế.



---

## Nguyên lý hoạt động

Bước 1: Chuẩn bị tập mẫu

Mỗi mệnh giá gồm:

templates/

├── 10000.jpg

├── 20000.jpg

├── 50000.jpg

├── 100000.jpg

├── 200000.jpg

├── 500000.jpg


---

Bước 2: Trích xuất đặc trưng ORB

orb = cv2.ORB_create(5000)

kp, des = orb.detectAndCompute(image, None)

Kết quả:

Keypoints

Descriptors



---

Bước 3: So khớp đặc trưng

Sử dụng BFMatcher:

bf = cv2.BFMatcher(cv2.NORM_HAMMING)

matches = bf.knnMatch(des_template,
                      des_scene,
                      k=2)

Lọc bằng Lowe Ratio Test:

if m.distance < 0.75 * n.distance:
    good.append(m)


---

Bước 4: Tính Homography

H, mask = cv2.findHomography(
    src_pts,
    dst_pts,
    cv2.RANSAC,
    5.0
)

Mục đích:

Loại bỏ điểm khớp sai.

Tìm phép biến đổi hình học.



---

Bước 5: Xác định vị trí tờ tiền

dst = cv2.perspectiveTransform(
    corners,
    H
)

Kết quả:

Tọa độ 4 góc của tờ tiền trong ảnh.



---

Bước 6: Vẽ Bounding Box

cv2.polylines(
    image,
    [np.int32(dst)],
    True,
    (0,255,0),
    3
)


---

Bước 7: Tính tổng tiền

Ví dụ:
10.000 VND : 1
20.000 VND : 1
50.000 VND : 1
100.000 VND : 1
200.000 VND : 1
500.000 VND : 1

Tổng:

880.000 VND


---

## Lưu đồ thuật toán

Ảnh đầu vào -> Tiền xử lý ảnh -> Trích xuất ORB -> So khớp đặc trưng -> Homography ->  Xác định vị trí tiền -> Vẽ Bounding Box -> Nhận dạng mệnh giá -> Tính tổng tiền -> Kết quả


---

## Kết quả thực nghiệm

Ví dụ hệ thống nhận dạng:

Mệnh giá	Số lượng

10.000	1

20.000	1

50.000	1

100.000	1

200.000	1

500.000	1



Tổng:


880.000 VNĐ


Hệ thống đồng thời hiển thị Bounding Box cho từng tờ tiền.


---

## Ưu điểm

Không cần huấn luyện dữ liệu.

Chạy nhanh.

Hoạt động tốt với ảnh xoay góc.

Dễ triển khai trên máy tính cấu hình thấp.



---

## Nhược điểm

Giảm độ chính xác khi tiền bị che khuất nhiều.

Nhạy với ánh sáng quá mạnh hoặc quá yếu.

Cần ảnh mẫu cho từng mệnh giá.



---

## Hướng phát triển

Kết hợp OCR để đọc trực tiếp mệnh giá.

Sử dụng SIFT hoặc AKAZE.

Nâng cấp sang YOLOv8 để tăng độ chính xác.

Xây dựng hệ thống đếm tiền thời gian thực từ camera.



---

## Tài liệu tham khảo

1. OpenCV Documentation


2. Rublee, Ethan et al. "ORB: An Efficient Alternative to SIFT or SURF", ICCV 2011.


3. OpenCV Feature Matching Tutorial


4. OpenCV Homography Tutorial


5. Digital Image Processing – Gonzalez & Woods
_______
