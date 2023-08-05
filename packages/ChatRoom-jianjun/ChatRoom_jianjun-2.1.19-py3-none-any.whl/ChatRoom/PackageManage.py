import os

class PackageManage():

    def __init__(self, user):

        self.user = user
        self.root_path = ".User"
        self.package_parh = os.path.join(self.root_path, "Package")
        if not os.path.exists(self.package_parh):
            os.makedirs(self.package_parh)



if __name__ == "__main__":

    pac = PackageManage()