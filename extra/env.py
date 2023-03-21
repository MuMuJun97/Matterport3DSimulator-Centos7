import os
import sys 
from pathlib import Path 
if __name__ == '__main__':
    root_dir = Path(__file__).parent
    pro_dir = root_dir.parent.resolve()
    print("[INFO] Project root dir: {}".format(pro_dir))
    file_lists = [
        'epoxy.pc','glm.pc','jsoncpp.pc'
    ]
    for file in file_lists:
        file = (root_dir / file).resolve().__str__()
        print('[INFO] read file: ',file)
        with open(file,'r') as f:
            data = f.readlines()
        if 'epoxy' in file:
            cfg_content = "prefix={}/extra/epoxy\n".format(str(pro_dir))
        elif 'glm' in file:
            cfg_content = "prefix={}/extra/GLM\n".format(str(pro_dir))
        elif 'jsoncpp' in file:
            cfg_content = "prefix={}/extra/jsoncpp\n".format(str(pro_dir))
        else:
            raise NotImplementedError
        data[0] = cfg_content
        with open(file,'w') as f:
            f.writelines(data)
    print("[INFO] Change ENV Success.")
        