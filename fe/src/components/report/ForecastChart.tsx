import { useRef, useEffect } from "react";
import type { ForecastData } from "../../services/api";

interface Props {
  forecast: ForecastData;
}

/**
 * Vẽ biểu đồ dự báo LSTM (nhiệt độ / giá Bitcoin) bằng Canvas.
 * Hiển thị 2 đường: actual (xanh) và forecast (cam).
 */
export const ForecastChart = ({ forecast }: Props) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // Hi-DPI support
    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    ctx.scale(dpr, dpr);
    const W = rect.width;
    const H = rect.height;

    // Data
    const actual = forecast.actual_values;
    const predicted = forecast.forecast_values;
    const allValues = [...actual, ...predicted];
    const totalPoints = allValues.length;

    if (totalPoints === 0) return;

    // Padding
    const padTop = 40;
    const padBottom = 50;
    const padLeft = 60;
    const padRight = 20;
    const chartW = W - padLeft - padRight;
    const chartH = H - padTop - padBottom;

    // Scales
    const minVal = Math.min(...allValues) * 0.995;
    const maxVal = Math.max(...allValues) * 1.005;
    const valRange = maxVal - minVal || 1;

    const xStep = chartW / Math.max(totalPoints - 1, 1);
    const toX = (i: number) => padLeft + i * xStep;
    const toY = (v: number) => padTop + chartH - ((v - minVal) / valRange) * chartH;

    // Clear
    ctx.clearRect(0, 0, W, H);

    // Background
    ctx.fillStyle = "#f8fafc";
    ctx.fillRect(0, 0, W, H);

    // Grid lines
    ctx.strokeStyle = "#e2e8f0";
    ctx.lineWidth = 1;
    const gridLines = 5;
    for (let i = 0; i <= gridLines; i++) {
      const y = padTop + (chartH / gridLines) * i;
      ctx.beginPath();
      ctx.moveTo(padLeft, y);
      ctx.lineTo(W - padRight, y);
      ctx.stroke();

      // Y-axis labels
      const val = maxVal - (valRange / gridLines) * i;
      ctx.fillStyle = "#64748b";
      ctx.font = "11px Inter, system-ui, sans-serif";
      ctx.textAlign = "right";
      ctx.fillText(val.toFixed(1), padLeft - 8, y + 4);
    }

    // Divider line between actual and forecast
    if (actual.length > 0 && predicted.length > 0) {
      const divX = toX(actual.length - 1);
      ctx.setLineDash([4, 4]);
      ctx.strokeStyle = "#94a3b8";
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(divX, padTop);
      ctx.lineTo(divX, padTop + chartH);
      ctx.stroke();
      ctx.setLineDash([]);

      // Label
      ctx.fillStyle = "#64748b";
      ctx.font = "10px Inter, system-ui, sans-serif";
      ctx.textAlign = "center";
      ctx.fillText("Hiện tại", divX, padTop + chartH + 14);
    }

    // Draw actual line (blue gradient)
    if (actual.length > 1) {
      // Fill area
      ctx.beginPath();
      ctx.moveTo(toX(0), toY(actual[0]));
      for (let i = 1; i < actual.length; i++) {
        ctx.lineTo(toX(i), toY(actual[i]));
      }
      ctx.lineTo(toX(actual.length - 1), padTop + chartH);
      ctx.lineTo(toX(0), padTop + chartH);
      ctx.closePath();
      const grad = ctx.createLinearGradient(0, padTop, 0, padTop + chartH);
      grad.addColorStop(0, "rgba(59, 130, 246, 0.2)");
      grad.addColorStop(1, "rgba(59, 130, 246, 0.02)");
      ctx.fillStyle = grad;
      ctx.fill();

      // Line
      ctx.beginPath();
      ctx.moveTo(toX(0), toY(actual[0]));
      for (let i = 1; i < actual.length; i++) {
        ctx.lineTo(toX(i), toY(actual[i]));
      }
      ctx.strokeStyle = "#3b82f6";
      ctx.lineWidth = 2;
      ctx.stroke();
    }

    // Draw forecast line (orange gradient)
    if (predicted.length > 0) {
      const offset = actual.length > 0 ? actual.length - 1 : 0;
      const startVal = actual.length > 0 ? actual[actual.length - 1] : predicted[0];

      // Fill area
      ctx.beginPath();
      ctx.moveTo(toX(offset), toY(startVal));
      for (let i = 0; i < predicted.length; i++) {
        ctx.lineTo(toX(offset + i + (actual.length > 0 ? 1 : 0)), toY(predicted[i]));
      }
      const lastX = toX(offset + predicted.length);
      ctx.lineTo(lastX, padTop + chartH);
      ctx.lineTo(toX(offset), padTop + chartH);
      ctx.closePath();
      const grad = ctx.createLinearGradient(0, padTop, 0, padTop + chartH);
      grad.addColorStop(0, "rgba(249, 115, 22, 0.2)");
      grad.addColorStop(1, "rgba(249, 115, 22, 0.02)");
      ctx.fillStyle = grad;
      ctx.fill();

      // Line
      ctx.beginPath();
      ctx.moveTo(toX(offset), toY(startVal));
      for (let i = 0; i < predicted.length; i++) {
        ctx.lineTo(toX(offset + i + (actual.length > 0 ? 1 : 0)), toY(predicted[i]));
      }
      ctx.strokeStyle = "#f97316";
      ctx.lineWidth = 2;
      ctx.setLineDash([6, 3]);
      ctx.stroke();
      ctx.setLineDash([]);
    }

    // Legend
    const legendY = padTop - 20;
    ctx.font = "12px Inter, system-ui, sans-serif";

    // Actual legend
    ctx.fillStyle = "#3b82f6";
    ctx.fillRect(padLeft, legendY - 4, 16, 3);
    ctx.fillStyle = "#334155";
    ctx.textAlign = "left";
    ctx.fillText("Thực tế", padLeft + 22, legendY);

    // Forecast legend
    ctx.fillStyle = "#f97316";
    ctx.fillRect(padLeft + 90, legendY - 4, 16, 3);
    ctx.fillStyle = "#334155";
    ctx.fillText("Dự báo (LSTM)", padLeft + 112, legendY);

    // Unit label
    ctx.fillStyle = "#94a3b8";
    ctx.font = "11px Inter, system-ui, sans-serif";
    ctx.textAlign = "left";
    ctx.fillText(forecast.unit, padLeft, padTop - 6);

  }, [forecast]);

  return (
    <div className="mt-8">
      <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
        <span className="w-2 h-2 rounded-full bg-orange-500 inline-block"></span>
        {forecast.title}
      </h3>
      <div className="bg-gray-50 rounded-xl p-4 border border-gray-100">
        <canvas
          ref={canvasRef}
          style={{ width: "100%", height: "300px" }}
          className="w-full"
        />
        <p className="text-xs text-gray-400 mt-2 text-center">
          Dự báo từ mô hình LSTM được huấn luyện trên dữ liệu lịch sử • Kết quả mang tính tham khảo
        </p>
      </div>
    </div>
  );
};
