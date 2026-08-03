import cv2
import numpy as np
import os

# =========================
# Đọc ảnh đầu vào
# =========================

img = cv2.imread("money.jpg")

if img is None:
    print("Không tìm thấy ảnh money.jpg")
    exit()

gray_scene = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# =========================
# ORB
# =========================

orb = cv2.ORB_create(5000)

kp_scene, des_scene = orb.detectAndCompute(
    gray_scene,
    None
)

bf = cv2.BFMatcher(cv2.NORM_HAMMING)

# =========================
# Biến lưu kết quả
# =========================

tong_tien = 0

so_luong = {}

detected_centers = []

# =========================
# Duyệt các template
# =========================

for file in os.listdir("templates"):

    path = os.path.join("templates", file)

    template = cv2.imread(path)

    if template is None:
        continue

    value = int(file.split(".")[0])

    gray_template = cv2.cvtColor(
        template,
        cv2.COLOR_BGR2GRAY
    )

    kp_temp, des_temp = orb.detectAndCompute(
        gray_template,
        None
    )

    if des_temp is None:
        continue

    matches = bf.knnMatch(
        des_temp,
        des_scene,
        k=2
    )

    good = []

    for m, n in matches:

        if m.distance < 0.75 * n.distance:
            good.append(m)

    if len(good) < 20:
        continue

    src_pts = np.float32(
        [kp_temp[m.queryIdx].pt for m in good]
    ).reshape(-1, 1, 2)

    dst_pts = np.float32(
        [kp_scene[m.trainIdx].pt for m in good]
    ).reshape(-1, 1, 2)

    H, mask = cv2.findHomography(
        src_pts,
        dst_pts,
        cv2.RANSAC,
        5.0
    )

    if H is None:
        continue

    h, w = gray_template.shape

    corners = np.float32([
        [0, 0],
        [0, h - 1],
        [w - 1, h - 1],
        [w - 1, 0]
    ]).reshape(-1, 1, 2)

    projected = cv2.perspectiveTransform(
        corners,
        H
    )

    center_x = int(np.mean(projected[:, 0, 0]))
    center_y = int(np.mean(projected[:, 0, 1]))

    duplicate = False

    for cx, cy in detected_centers:

        distance = np.sqrt(
            (center_x - cx) ** 2 +
            (center_y - cy) ** 2
        )

        if distance < 80:
            duplicate = True
            break

    if duplicate:
        continue

    detected_centers.append(
        (center_x, center_y)
    )

    if value not in so_luong:
        so_luong[value] = 0

    so_luong[value] += 1

    tong_tien += value

    cv2.polylines(
        img,
        [np.int32(projected)],
        True,
        (0, 255, 0),
        3
    )

    cv2.putText(
        img,
        f"{value:,} VND",
        (center_x - 50, center_y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 0, 255),
        2
    )

# =========================
# In thống kê
# =========================

print("\n===== THỐNG KÊ =====")

for value in sorted(so_luong):

    print(
        f"{value:,} VND : {so_luong[value]} tờ"
    )
print("--------------------")
print(
    f"TỔNG TIỀN: {tong_tien:,} VND"
)
print("--------------------")

# =========================
# Hiển thị tổng tiền
# =========================

cv2.putText(
    img,
    f"TOTAL: {tong_tien:,} VND",
    (20, 50),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    (255, 0, 0),
    3
)

cv2.imwrite("result.jpg", img)

cv2.imshow("Money Counter", img)

cv2.waitKey(0)
cv2.destroyAllWindows()    
