# Note:

1. 工作文件夹为工程根目录而非脚本所在目录。
2. news文件夹中保留了2022年4月的数据供测试使用。如需运行爬虫爬取信息则需要清空news文件夹中的csv文件（不要删除segmented文件夹）。
3. 以下位置有进程数设置，运行前需根据运行平台的性能进行调整。

   ```plaintext
   ./0_spyder/main_laucher.py    第15行
   ./1_merger/0_fenci_func.py    第86行
   ./2_modeler/1_ldamodeling.py  第151行、第162行
   ```
4. 运行爬虫前需在./0_spyder/spyder.py文件中13-16行根据运行平台设置浏览器类型、工作方式、浏览器可执行程序路径和驱动程序路径。utils文件夹中已包含amd64 linux适用的firefox驱动程序。
5. 运行顺序参考run.sh，建议使用该脚本自动执行。
6. 由于样本较大，程序运行耗时较长，请耐心等待（或者睡一觉）。
