import { ImageBase, ImageBaseView } from "./image_base";
import { isArray } from "../../core/util/types";
export class ImageRGBAView extends ImageBaseView {
    static __name__ = "ImageRGBAView";
    _flat_img_to_buf8(img, _length_divisor) {
        let array;
        if (isArray(img)) {
            array = new Uint32Array(img);
        }
        else {
            array = img;
        }
        return new Uint8ClampedArray(array.buffer);
    }
}
export class ImageRGBA extends ImageBase {
    static __name__ = "ImageRGBA";
    constructor(attrs) {
        super(attrs);
    }
    static {
        this.prototype.default_view = ImageRGBAView;
    }
}
//# sourceMappingURL=image_rgba.js.map