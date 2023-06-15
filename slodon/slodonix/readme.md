Well, as you can see in the [introduction](https://github.com/FlurryGlo/slodon/blob/hels15/etc/slodon.pdf), we need to deal with GUI interactions. 
To handle this, we utilize a sub-library which effectively manages all the necessary GUI operations. [Xlib](https://www.x.org/wiki/) is like the go-to library here, but the python version is quite out-dated. 
Thus, we develop the `slodonix` library, which is a wrapper around  [Xlib](https://www.x.org/wiki/) and provides a more pythonic interface.

---
This sub-lib can be an independent library in the future.

The corresponding [MIRO TABLE](https://miro.com/app/board/uXjVMCWiS68=/?share_link_id=600250455221)
