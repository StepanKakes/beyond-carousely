// Najde obličeje (a hlavy/postavy) na fotkách přes Apple Vision.
// Použití: swift tvare.swift foto1.jpg foto2.jpg ...
// Výstup: JSON {cesta: {"w":..,"h":..,"tvare":[[x,y,w,h],..],"postavy":[[x,y,w,h],..]}}
// Souřadnice jsou normalizované 0..1, počátek vlevo nahoře, po otočení podle EXIF.
import Foundation
import Vision
import ImageIO

var vysledek: [String: Any] = [:]
for cesta in CommandLine.arguments.dropFirst() {
    let url = URL(fileURLWithPath: cesta)
    guard let src = CGImageSourceCreateWithURL(url as CFURL, nil),
          let img = CGImageSourceCreateImageAtIndex(src, 0, nil) else { continue }
    let props = CGImageSourceCopyPropertiesAtIndex(src, 0, nil) as? [CFString: Any]
    let o = (props?[kCGImagePropertyOrientation] as? UInt32) ?? 1
    let orient = CGImagePropertyOrientation(rawValue: o) ?? .up
    var w = img.width, h = img.height
    if [5, 6, 7, 8].contains(o) { swap(&w, &h) }
    let tvare = VNDetectFaceRectanglesRequest()
    let postavy = VNDetectHumanRectanglesRequest()
    postavy.upperBodyOnly = true
    let handler = VNImageRequestHandler(cgImage: img, orientation: orient, options: [:])
    try? handler.perform([tvare, postavy])
    func prevod(_ b: CGRect) -> [Double] { [Double(b.minX), Double(1 - b.maxY), Double(b.width), Double(b.height)] }
    vysledek[cesta] = [
        "w": w, "h": h,
        "tvare": (tvare.results ?? []).map { prevod($0.boundingBox) },
        "postavy": (postavy.results ?? []).map { prevod($0.boundingBox) },
    ]
}
let data = try JSONSerialization.data(withJSONObject: vysledek, options: [.prettyPrinted])
print(String(data: data, encoding: .utf8)!)
