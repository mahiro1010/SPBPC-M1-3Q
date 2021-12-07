import numpy as np
import sys

# 微分・値更新用のクラス
class UpdateValue:
    def __init__(self, p, q, x, w, alpha) -> None:
        self.p = p
        self.q = q
        self.x = x
        self.w = w
        self.alpha = alpha
        self.epsilon = 0.1

    def __differential(self, i, j):
        dki_dw = 0
        for x1 in range(2):
            for x3 in range(2):
                dki_dw += float((-1)) * self.__q_x1(x1) * self.__q_x3_d_x1(x3, x1) * (self.__p_x2_d_x1_x3(x1, x3) - self.__p_x2_x3_d_x1(x1))
                print(self.__p_x2_d_x1_x3(x1, x3) - self.__p_x2_x3_d_x1(x1))
                print(self.__p_x2_d_x1_x3(x1, x3))
                print(self.__p_x2_x3_d_x1(x1))
                
        return (-1) * self.alpha * self.x[i] * self.x[j] * dki_dw

    def __q_x1(self, x1):
        val = 0
        for x2 in range(2):
            for x3 in range(2):
                val += self.q[x1, x2, x3]
        return val

    def __q_x3_d_x1(self, x3, x1):
        top = 0
        bottom = 0
        for x2_ in range(2):
            top += self.q[x1, x2_, x3]

        for x2_ in range(2):
            for x3_ in range(2):
                bottom += self.q[x1, x2_, x3_]
        return top / bottom

    def __p_x2_d_x1_x3(self, x1, x3):
        val = 0
        top = 0
        bottom = 0
        for x2_ in range(2):
            top = self.p[x1, x2_, x3]
            bottom = 0
            for x2__ in range(2):
                bottom += self.p[x1, x2__, x3]
            val = top / bottom
        return val

    def __p_x2_x3_d_x1(self, x1):
        val = 0
        top = 0
        bottom = 0
        for x2_ in range(2):
            for x3_ in range(2):
                top = self.p[x1, x2_, x3_]
                bottom = 0
                for x2__ in range(2):
                    for x3__ in range(2):
                        bottom += self.p[x1, x2__, x3__]
                val += top / bottom
        return val

    def __update_stop(self, w_old, w_new, threshold=10*(-10)):
        if threshold > np.abs(w_new - w_old):
            return True
        else:
            return False

    def update(self, i, j):
        if i == j:
            self.w[i, j] = 0
            return 0
        count = 0
        while True :
            w_old = self.w[i, j].copy()
            w_new = self.w[i, j] - self.epsilon * self.__differential(i, j)
            if self.__update_stop(w_old, w_new):
                return 0
            else:
                self.w[i, j] = w_new
                count += 1
                if count > 10:
                    sys.exit()

if __name__ == "__main__":
    # 同時確率を生成
    joint_p = np.random.rand(2, 2, 2)
    joint_p = joint_p / np.sum(joint_p)

    joint_q = np.random.rand(2, 2, 2)
    joint_q = joint_q / np.sum(joint_q)

    w = np.zeros((3, 3))
    x = np.ones((3))

    alpha = 0.00001

    update_w = UpdateValue(joint_p, joint_q, x, w, alpha)
    update_w.update(0,1)
    print(update_w.w[0, 1])