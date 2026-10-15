using Microsoft.VisualStudio.TestTools.UnitTesting;
using OrderPricing;

namespace OrderPricing.Tests;

[TestClass]
public class PriceCalculatorTests
{
    [TestMethod]
    public void Order_Sub0_Exception()
    {
        decimal subtotal = -1m;

        Assert.ThrowsException<ArgumentOutOfRangeException>(() => PriceCalculator.CalculateTotal(subtotal, false, false));
    }

    [TestMethod]
    public void Order_100001_Exception()
    {
        decimal subtotal = 100001m;

        Assert.ThrowsException<ArgumentOutOfRangeException>(() => PriceCalculator.CalculateTotal(subtotal, false, false));
    }

    [TestMethod]
    public void Order_0_TotalIs300()
    {
        decimal subtotal = 0m;
        decimal expected = 300m;

        decimal actual = PriceCalculator.CalculateTotal(subtotal, false, false);

        Assert.AreEqual(expected, actual);
    }

    [TestMethod]
    public void Order_100000WithoutLoyalty_TotalIs95000()
    {
        decimal subtotal = 100000m;
        decimal expected = 95000m;

        decimal actual = PriceCalculator.CalculateTotal(subtotal, false, false);

        Assert.AreEqual(expected, actual);
    }

    [TestMethod]
    public void Order_1000WithoutLoyalty_TotalIs1300()
    {
        decimal subtotal = 1000m;
        decimal expected = 1300m;

        decimal actual = PriceCalculator.CalculateTotal(subtotal, false, false);

        Assert.AreEqual(expected, actual);
    }

    [TestMethod]
    public void Order_5000WithoutLoyalty_TotalIs4750()
    {
        decimal subtotal = 5000m;
        decimal expected = 4750m;

        decimal actual = PriceCalculator.CalculateTotal(subtotal, false, false);

        Assert.AreEqual(expected, actual);
    }

    [TestMethod]
    public void Order_5001WithoutLoyalty_TotalIs4750_95()
    {
        decimal subtotal = 5001m;
        decimal expected = 4750.95m;

        decimal actual = PriceCalculator.CalculateTotal(subtotal, false, false);

        Assert.AreEqual(expected, actual);
    }

    [TestMethod]
    public void Order_4000WithoutLoyalty_TotalIs4000()
    {
        decimal subtotal = 4000m;
        decimal expected = 4000m;

        decimal actual = PriceCalculator.CalculateTotal(subtotal, false, false);

        Assert.AreEqual(expected, actual);
    }

    [TestMethod]
    public void Order_3999WithoutLoyalty_TotalIs4299()
    {
        decimal subtotal = 3999m;
        decimal expected = 4299m;

        decimal actual = PriceCalculator.CalculateTotal(subtotal, false, false);

        Assert.AreEqual(expected, actual);
    }

    [TestMethod]
    public void Order_4000WithLoyalty_TotalIs3600()
    {
        decimal subtotal = 4000m;
        decimal expected = 3600m;

        decimal actual = PriceCalculator.CalculateTotal(subtotal, true, false);

        Assert.AreEqual(expected, actual);
    }

    [TestMethod]
    public void Order_4000WithoutLoyalty_Express_TotalIs4500()
    {
        decimal subtotal = 4000m;
        decimal expected = 4500m;

        decimal actual = PriceCalculator.CalculateTotal(subtotal, false, true);

        Assert.AreEqual(expected, actual);
    }

    [TestMethod]
    public void Order_50000WithLoyalty_Express_TotalIs45500()
    {
        decimal subtotal = 50000m;
        decimal expected = 45500m;

        decimal actual = PriceCalculator.CalculateTotal(subtotal, true, true);

        Assert.AreEqual(expected, actual);
    }
}
