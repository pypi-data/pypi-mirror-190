# Copyright 2022 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================

"""Defines nn operators with functional form."""
from __future__ import absolute_import
from math import pi, log

import mindspore.ops as ops
from mindspore.ops.primitive import constexpr
from mindspore.ops import operations as P
from mindspore.ops.operations import _inner_ops as inner
from mindspore.ops.operations import nn_ops as NN_OPS
from mindspore.ops.operations import image_ops as IMG
import mindspore.common.dtype as mstype
from mindspore.ops.function.math_func import logsumexp
from mindspore.common.tensor import Tensor
from mindspore._c_expression import Tensor as Tensor_
from mindspore.ops._primitive_cache import _get_cache_prim
from mindspore._checkparam import Rel
from mindspore._checkparam import Validator as validator
from mindspore.ops.composite.multitype_ops._constexpr_utils import raise_value_error
from mindspore.ops.operations.nn_ops import MaxUnpool2D, MaxUnpool3D
from mindspore.ops.operations.nn_ops import FractionalMaxPoolWithFixedKsize, FractionalMaxPool3DWithFixedKsize
from mindspore.ops.operations.nn_ops import PadV3

slice_ = P.Slice()
fast_gelu_ = P.FastGeLU()
softsign_ = P.Softsign()
hardswish_ = P.HSwish()
mish_ = NN_OPS.Mish()
selu_ = NN_OPS.SeLU()
scalar_to_tensor_ = P.ScalarToTensor()
sigmoid_ = NN_OPS.Sigmoid()


def adaptive_avg_pool2d(input_x, output_size):
    r"""
    This operator applies a 2D adaptive average pooling to an input signal composed of multiple input planes.
    That is, for any input size, the size of the specified output is H x W.
    The number of output features is equal to the number of input features.

    The input and output data format can be "NCHW" and "CHW". N is the batch size, C is the number of channels,
    H is the feature height, and W is the feature width.

    For adaptive average pooling for 2D:

    ..  math::
        \begin{align}
        h_{start} &= floor(i * H_{in} / H_{out})\\
        h_{end} &= ceil((i + 1) * H_{in} / H_{out})\\
        w_{start} &= floor(j * W_{in} / W_{out})\\
        w_{end} &= ceil((j + 1) * W_{in} / W_{out})\\
        Output(i,j) &= \frac{\sum Input[h_{start}:h_{end}, w_{start}:w_{end}]}{(h_{end}- h_{start})
        * (w_{end}- w_{start})}
        \end{align}

    Args:
        input_x (Tensor): The input of adaptive_avg_pool2d, which is a 3D or 4D tensor,
          with float16, float32 or float64 data type.
        output_size (Union[int, tuple]): The target output size is H x W.
            `ouput_size` can be a tuple consisted of int type H and W, or a single H for H x H, or None.
            If it is None, it means the output size is the same as the input size.

    Returns:
        Tensor, with the same type as the `input_x`.

        Shape of the output is `input_x_shape[:len(input_x_shape) - len(out_shape)] + out_shape`.

    .. math::

        out\_shape = \begin{cases}
        input\_x\_shape[-2] + output\_size[1], & \text{if output_size is (None, w);}\\
        output\_size[0] + input\_x\_shape[-1], & \text{if output_size is (h, None);}\\
        input\_x\_shape[-2:], & \text{if output_size is (None, None);}\\
        (h, h), & \text{if output_size is h;}\\
        (h, w), & \text{if output_size is (h, w)}
        \end{cases}

    Raises:
        ValueError: If `output_size` is a tuple and the length of `output_size` is not 2.
        TypeError: If `input_x` is not a Tensor.
        TypeError: If dtype of `input_x` is not float16, float32 or float64.
        ValueError: If the dimension of `input_x` is less than or equal to the dimension of `output_size`.

    Supported Platforms:
        ``GPU``

    Examples:
        >>> # case 1: output_size=(None, 2)
        >>> input_x = Tensor(np.array([[[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]],
        ...                            [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]],
        ...                            [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]]), mindspore.float32)
        >>> output = ops.adaptive_avg_pool2d(input_x, (None, 2))
        >>> print(output)
        [[[1.5 2.5]
          [4.5 5.5]
          [7.5 8.5]]
         [[1.5 2.5]
          [4.5 5.5]
          [7.5 8.5]]
         [[1.5 2.5]
          [4.5 5.5]
          [7.5 8.5]]]
        >>> # case 2: output_size=2
        >>> output = ops.adaptive_avg_pool2d(input_x, 2)
        >>> print(output)
        [[[3. 4.]
          [6. 7.]]
         [[3. 4.]
          [6. 7.]]
         [[3. 4.]
          [6. 7.]]]
        >>> # case 3: output_size=(1, 2)
        >>> output = ops.adaptive_avg_pool2d(input_x, (1, 2))
        >>> print(output)
        [[[4.5 5.5]]
         [[4.5 5.5]]
         [[4.5 5.5]]]
    """
    adaptive_avgpool2d_ = _get_cache_prim(P.AdaptiveAvgPool2D)(output_size)
    return adaptive_avgpool2d_(input_x)


def adaptive_avg_pool3d(input_x, output_size):
    r"""
    This operator applies a 3D adaptive average pooling to an input signal composed of multiple input planes.
    That is, for any input size, the size of the specified output is :math:`(D, H, W)`.
    The number of output features is equal to the number of input planes.

    Suppose the last 3 dimension size of x is :math:`(inD, inH, inW)`, the last 3 dimension size of output is
    :math:`(outD, outH, outW)`.

    .. math::
        \begin{array}{ll} \\
            \forall \quad od \in [0,outD-1], oh \in [0,outH-1], ow \in [0,outW-1]\\
            output[od,oh,ow] = \\
            \qquad mean(x[istartD:iendD+1,istartH:iendH+1,istartW:iendW+1])\\
            where,\\
            \qquad istartD= \left\lceil \frac{od * inD}{outD} \right\rceil \\
            \qquad iendD=\left\lfloor \frac{(od+1)* inD}{outD} \right\rfloor \\
            \qquad istartH=\left\lceil \frac{oh * inH}{outH} \right\rceil \\
            \qquad iendH=\left\lfloor \frac{(oh+1) * inH}{outH} \right\rfloor \\
            \qquad istartW=\left\lceil \frac{ow * inW}{outW} \right\rceil \\
            \qquad iendW=\left\lfloor \frac{(ow+1) * inW}{outW} \right\rfloor
        \end{array}

    Args:
        input_x (Tensor): The input of adaptive_avg_pool3d, which is a 5D or 4D Tensor.
        output_size (Union[int, tuple]): The target output size. `ouput_size` can be a tuple :math:`(D, H, W)`,
            or an int D for :math:`(D, D, D)`. :math:`D`, :math:`H` and :math:`W` can be int or None
            which means the output size is the same as that of the input.

    Returns:
        Tensor, with the same type as the `input_x`.

    Raises:
        TypeError: If `input_x` is not a Tensor.
        TypeError: If dtype of `input_x` is not float16, float32 or float64.
        ValueError: If the dimension of `input_x` is not 4D or 5D.
        ValueError: If `output_size` value is not positive.

    Supported Platforms:
        ``GPU`` ``CPU``

    Examples:
        >>> # case 1: output_size=(3, 3, 4)
        >>> output_size=(3, 3, 4)
        >>> input_x_val = np.random.randn(4, 3, 5, 6, 7)
        >>> input_x = Tensor(input_x_val, mindspore.float32)
        >>> output = ops.adaptive_avg_pool3d(input_x, output_size)
        >>> print(output.shape)
        (4, 3, 3, 3, 4)
        >>> # case 2: output_size=4
        >>> output_size=5
        >>> input_x_val = np.random.randn(2, 3, 8, 6, 12)
        >>> input_x = Tensor(input_x_val, mindspore.float32)
        >>> output = ops.adaptive_avg_pool3d(input_x, output_size)
        >>> print(output.shape)
        (2, 3, 5, 5, 5)
        >>> # case 3: output_size=(None, 4, 5)
        >>> output_size=(None, 4, 5)
        >>> input_x_val = np.random.randn(4, 1, 9, 10, 8)
        >>> input_x = Tensor(input_x_val, mindspore.float32)
        >>> output = ops.adaptive_avg_pool3d(input_x, output_size)
        >>> print(output.shape)
        (4, 1, 9, 4, 5)
    """
    adaptive_avg_pool3d_ = _get_cache_prim(NN_OPS.AdaptiveAvgPool3D)(output_size)
    return adaptive_avg_pool3d_(input_x)


@constexpr
def _check_avgpool_1d_type_and_int(kernel_size, stride, ceil_mode, count_include_pad):
    """Checks the type of avgpool1d input"""
    validator.check_value_type('kernel_size', kernel_size, [int], 'avg_pool1d')
    validator.check_value_type('stride', stride, [int], 'avg_pool1d')
    validator.check_value_type('ceil_mode', ceil_mode, bool, 'avg_pool1d')
    validator.check_value_type('count_include_pad', count_include_pad, bool, 'avg_pool1d')
    validator.check_int(kernel_size, 1, Rel.GE, "kernel_size", 'avg_pool1d')
    validator.check_int(stride, 1, Rel.GE, "stride", 'avg_pool1d')


@constexpr
def check_non_negative_int(arg_value, arg_name=None, prim_name=None):
    """Check argument is non-negative integer, which mean arg_value >= 0."""
    validator.check_non_negative_int(arg_value, arg_name, prim_name)


def avg_pool1d(input_x, kernel_size=1, stride=1, padding=0, ceil_mode=False, count_include_pad=True):
    r"""
    Applies a 1D average pooling over an input Tensor which can be regarded as a composition of 1D input planes.

    Typically the input is of shape :math:`(N_{in}, C_{in}, L_{in})`, avg_pool1d outputs regional average in the
    :math:`(L_{in})`-dimension. Given kernel size :math:`ks = l_{ker}` and `stride` :math:`s = s_0`, the
    operation is as follows.

    .. math::
        \text{output}(N_i, C_j, l) = \frac{1}{l_{ker}} \sum_{n=0}^{l_{ker}-1}
        \text{input}(N_i, C_j, s_0 \times l + n)

    .. warning::
        `kernel_size` is in the range `[1, 255]`. `stride` is in the range `[1, 63]`.

    Args:
        input_x (Tensor): Tensor of shape :math:`(N, C_{in}, L_{in})`.
        kernel_size (int): The size of kernel window used to take the average value, Default: 1.
        stride (int): The distance of kernel moving, an int number that represents the height and
            width of movement are both strides, or a tuple of two int numbers that represent height and width of
            movement respectively. Default: 1.
        padding (Union(int, tuple[int])): The pad value to be filled. If `padding` is an integer, the paddings of left
            and right are the same, equal to pad. If `padding` is a tuple of `2` integers, the padding of left and right
            equal to `padding[0]` and `padding[1]` correspondingly. Default: 0.
        ceil_mode (bool): If True, apply ceil instead of floor to compute the output shape. Default: False.
        count_include_pad (bool): If True, include the zero-padding in the averaging calculation. Default: True.

    Returns:
        Tensor of shape :math:`(N, C_{out}, L_{out})`.

    Raises:
        TypeError: If `input_x` is not an Tensor.
        TypeError: If `kernel_size` or `stride` is not an int.
        TypeError: If `ceil_mode` or `count_include_pad` is not a bool.
        ValueError: If length of shape of `input_x` is not equal to `3`.
        ValueError: If `kernel_size` or `stride` is less than `1`.
        ValueError: If `padding` is not int nor a tuple whose length is equal to `2`.
        ValueError: If value(s) of `padding` is less than `0`.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> input_x = Tensor(np.random.randint(0, 10, [1, 3, 6]), mindspore.float32)
        >>> output = ops.avg_pool1d(input_x, kernel_size=6, stride=1)
        >>> print(output.shape)
        (1, 3, 1)
    """
    if not isinstance(input_x, (Tensor, Tensor_)):
        raise TypeError("For avg_pool1d, the input input_x must be tensor")

    if len(input_x.shape) != 3:
        raise ValueError("For avg_pool1d, input must have 3 dim, but got {}.".format(len(input_x.shape)))

    _check_avgpool_1d_type_and_int(kernel_size, stride, ceil_mode, count_include_pad)
    if isinstance(padding, int):
        check_non_negative_int(padding, 'padding', 'avg_pool1d')
        padding = (0, 0, 0, 0, padding, padding)
    elif isinstance(padding, tuple):
        if len(padding) != 2:
            raise ValueError("For avg_pool1d, padding should be int or tuple of length 2.")
        for item in padding:
            check_non_negative_int(item, 'padding', 'avg_pool1d')
        padding = (0, 0, 0, 0, padding[0], padding[1])
    else:
        raise TypeError("For avg_pool1d, padding should be int or tuple of length 2.")

    expand_op = _get_cache_prim(P.ExpandDims)()
    squeeze_op = _get_cache_prim(P.Squeeze)((2, 3))
    avg_pool_op = _get_cache_prim(P.AvgPool3D)(kernel_size=(1, 1, kernel_size),
                                               strides=(1, 1, stride),
                                               pad_mode='pad',
                                               pad=padding,
                                               ceil_mode=ceil_mode,
                                               count_include_pad=count_include_pad)
    input_x = expand_op(input_x, 2)
    input_x = expand_op(input_x, 2)
    input_x = avg_pool_op(input_x)
    input_x = squeeze_op(input_x)
    return input_x


@constexpr
def _check_avgpool_2d_kernel_size(kernel_size):
    """check and calculate the avgpool2d kernel_size"""
    if isinstance(kernel_size, int):
        validator.check_int(kernel_size, 1, Rel.GE, "kernel_size", 'avg_pool2d')
        kernel_size = (1, kernel_size, kernel_size)
    elif isinstance(kernel_size, tuple):
        if len(kernel_size) != 2:
            raise ValueError("For avg_pool2d, kernel_size should be int or tuple of length 2.")
        for item in kernel_size:
            validator.check_int(item, 1, Rel.GE, "kernel_size", 'avg_pool2d')
        kernel_size = (1, kernel_size[0], kernel_size[1])
    else:
        raise TypeError("For avg_pool2d, kernel_size should be int or tuple of length 2.")
    return kernel_size


@constexpr
def _check_avgpool_2d_stride(stride):
    """check and calculate the avgpool2d stride"""
    if isinstance(stride, int):
        validator.check_int(stride, 1, Rel.GE, "stride", 'avg_pool2d')
        stride = (1, stride, stride)
    elif isinstance(stride, tuple):
        if len(stride) != 2:
            raise ValueError("For avg_pool2d, stride should be int or tuple of length 2.")
        for item in stride:
            validator.check_int(item, 1, Rel.GE, "stride", 'avg_pool2d')
        stride = (1, stride[0], stride[1])
    else:
        raise TypeError("For avg_pool2d, stride should be int or tuple of length 2.")
    return stride


@constexpr
def _check_avgpool_2d_padding(padding):
    """check and calculate the avgpool2d padding"""
    if isinstance(padding, int):
        validator.check_non_negative_int(padding, 'padding', 'avg_pool2d')
        padding = (0, 0, padding, padding, padding, padding)
    elif isinstance(padding, tuple):
        if len(padding) != 4:
            raise ValueError("For avg_pool2d, padding should be int or tuple of length 4.")
        for item in padding:
            validator.check_non_negative_int(item, 'padding', 'avg_pool2d')
        padding = (0, 0, padding[0], padding[1], padding[2], padding[3])
    else:
        raise TypeError("For avg_pool2d, padding should be int or tuple of length 4.")
    return padding


@constexpr
def _check_avg_pool2d_type_and_value(ceil_mode, count_include_pad, divisor_override):
    """check the type of avgpool2d input"""
    validator.check_value_type('ceil_mode', ceil_mode, bool, 'avg_pool2d')
    validator.check_value_type('count_include_pad', count_include_pad, bool, 'avg_pool2d')
    validator.check_non_negative_int(divisor_override, 'divisor_override', 'avg_pool2d')


def avg_pool2d(input_x, kernel_size=1, stride=1, padding=0, ceil_mode=False, count_include_pad=True,
               divisor_override=0):
    r"""
    Applies a 2D average pooling over an input Tensor which can be regarded as a composition of 2D input planes.
    Typically the input is of shape :math:`(N_{in}, C_{in}, H_{in}, W_{in})`, outputs regional average in the
    :math:`(H_{in}, W_{in})`-dimension. Given kernel size :math:`(k_{h}, k_{w})` and `strides` , the operation
    is as follows.

    .. math::
        \text{output}(N_i, C_j, h, w) = \frac{1}{k_{h} * k_{w}} \sum_{m=0}^{k_{h}-1} \sum_{n=0}^{k_{w}-1}
        \text{input}(N_i, C_j, stride[0] \times h + m, stride[1] \times w + n)

    .. warning::
        `kernel_size` is in the range `[1, 255]`. `stride` is in the range `[1, 63]`.

    Args:
        input_x (Tensor): Tensor of shape :math:`(N, C_{in}, H_{in}, W_{in})`.
        kernel_size (Union[int, tuple[int]]): The size of kernel used to take the average value. It is an int number
            that represents height and width of the kernel, or a tuple of two int numbers that represent height and
            width respectively. Default: 1.
        stride (Union[int, tuple[int]]): The distance of kernel moving, an int number that represents the height and
            width of movement are both strides, or a tuple of two int numbers that represent height and width of
            movement respectively. Default: 1.
        padding (Union(int, tuple[int])): The pad value to be filled. Default: 0. If `padding` is an integer, the
            paddings of top, bottom, left and right are the same, equal to pad. If `padding` is a tuple of `4` integers,
            the padding of top, bottom, left and right equal to `padding[0]`, `padding[1]`, `padding[2]` and
            `padding[3]` correspondingly. Default: 0.
        ceil_mode (bool): If True, apply ceil instead of floor to compute the output shape. Default: False.
        count_include_pad (bool): If True, include the zero-padding in the averaging calculation. Default: True.
        divisor_override (int): If specified, it will be used as divisor in the averaging calculation, otherwise
            `kernel_size` will be used. Default: 0.

    Returns:
        Tensor, with shape :math:`(N, C_{out}, H_{out}, W_{out})`.

    Raises:
        TypeError: If `input_x` is not an Tensor.
        TypeError: If `kernel_size` or `stride` is neither int nor tuple.
        TypeError: If `ceil_mode` or `count_include_pad` is not a bool.
        TypeError: If `divisor_override` is not an int.
        ValueError: If length of shape of `input_x` is not equal to `4`.
        ValueError: If `kernel_size` or `stride` is less than 1.
        ValueError: If `kernel_size` or `stride` is a tuple whose length is not equal to `2`.
        ValueError: If `padding` is not int nor a tuple whose length is equal to `4`.
        ValueError: If value(s) of `padding` is less than `0`.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> x = Tensor(np.arange(1 * 3 * 3 * 4).reshape(1, 3, 3, 4), mindspore.float32)
        >>> output = ops.avg_pool2d(x, kernel_size=2, stride=1)
        >>> print(output)
        [[[[ 2.5   3.5   4.5]
           [ 6.5   7.5   8.5]]
          [[14.5  15.5  16.5]
           [18.5  19.5  20.5]]
          [[26.5  27.5  28.5]
           [30.5  31.5  32.5]]]]
    """
    if not isinstance(input_x, (Tensor, Tensor_)):
        raise TypeError("For avg_pool2d, the input input_x must be tensor")

    if len(input_x.shape) != 4:
        raise ValueError("For avg_pool2d, input must have 4 dim, but got {}.".format(len(input_x.shape)))

    kernel_size = _check_avgpool_2d_kernel_size(kernel_size)
    stride = _check_avgpool_2d_stride(stride)
    padding = _check_avgpool_2d_padding(padding)
    _check_avg_pool2d_type_and_value(ceil_mode, count_include_pad, divisor_override)

    expand_op = _get_cache_prim(P.ExpandDims)()
    squeeze_op = _get_cache_prim(P.Squeeze)(2)
    avg_pool_op = _get_cache_prim(P.AvgPool3D)(kernel_size=kernel_size,
                                               strides=stride,
                                               pad_mode='pad',
                                               pad=padding,
                                               ceil_mode=ceil_mode,
                                               count_include_pad=count_include_pad,
                                               divisor_override=divisor_override)
    input_x = expand_op(input_x, 2)
    input_x = avg_pool_op(input_x)
    input_x = squeeze_op(input_x)
    return input_x


@constexpr
def _check_avg_pool3d_padding(padding):
    """Check the padding value in avg_pool3d op."""
    if isinstance(padding, int):
        validator.check_non_negative_int(padding, 'padding', 'avg_pool3d')
    elif isinstance(padding, tuple):
        if len(padding) != 6:
            raise ValueError("For avg_pool3d, padding should be int or tuple of length 6.")
        for item in padding:
            validator.check_non_negative_int(item, 'padding', 'avg_pool3d')
    else:
        raise TypeError("For avg_pool3d, padding should be int or tuple of length 6.")


def avg_pool3d(input_x, kernel_size=1, stride=1, padding=0, ceil_mode=False, count_include_pad=True,
               divisor_override=0):
    r"""
    Applies a 3D average pooling over an input Tensor which can be regarded as a composition of 3D input planes.
    Typically the input is of shape :math:`(N, C, D_{in}, H_{in}, W_{in})`, avg_pool3d outputs regional average in the
    :math:`(D_{in}, H_{in}, W_{in})`-dimension. Given kernel size :math:`ks = (d_{ker}, h_{ker}, w_{ker})` and stride
    :math:`s = (s_0, s_1, s_2)`, the operation is as follows.

    .. math::
        \text{output}(N_i, C_j, d, h, w) =
        \frac{1}{d_{ker} * h_{ker} * w_{ker}} \sum_{l=0}^{d_{ker}-1} \sum_{m=0}^{h_{ker}-1} \sum_{n=0}^{w_{ker}-1}

        \text{input}(N_i, C_j, s_0 \times d + l, s_1 \times h + m, s_2 \times w + n)
    .. warning::
        `kernel_size` is in the range `[1, 255]`. `stride` is in the range `[1, 63]`.

    Args:
        input_x (Tensor): Tensor of shape :math:`(N, C, D_{in}, H_{in}, W_{in})`. Currently support float16 and
            float32 data type.
        kernel_size (Union[int, tuple[int]]): The size of kernel used to take the average value, is an int number
            that represents depth, height and width are both `kernel_size`, or a tuple of three int numbers that
            represent depth, height and width respectively. Default: 1.
        stride (Union[int, tuple[int]]): The distance of kernel moving, an int number that represents the depth,
            height and width of movement are both stride, or a tuple of three int numbers that represent depth, height
            and width of movement respectively. Default: 1.
        padding (Union(int, tuple[int])): The pad value to be filled. If `padding` is an integer, the addings of head,
            tail, top, bottom, left and right are the same, equal to pad. If `padding` is a tuple of six integers, the
            padding of head, tail, top, bottom, left and right equal to padding[0], padding[1], padding[2],
            padding[3], padding[4] and padding[5] correspondingly. Default: 0
        ceil_mode (bool): If True, ceil instead of floor to compute the output shape. Default: False.
        count_include_pad (bool): If True, averaging calculation will include the zero-padding. Default: True.
        divisor_override (int): If specified, it will be used as divisor in the averaging calculation, otherwise
            `kernel_size` will be used. Default: 0.

    Returns:
        Tensor, with shape :math:`(N, C, D_{out}, H_{out}, W_{out})`. Has the same data type with `input_x`.

    Raises:
        TypeError: If `input_x` is not an Tensor.
        TypeError: If `kernel_size`, `stride` or `padding` is neither an int not a tuple.
        TypeError: If `ceil_mode` or `count_include_pad` is not a bool.
        TypeError: If `divisor_override` is not an int.
        ValueError: If length of shape of `input_x` is not equal to `5`.
        ValueError: If numbers in `kernel_size` or `stride` are not positive.
        ValueError: If `kernel_size` or `stride` is a tuple whose length is not equal to `3`.
        ValueError: If `padding` is a tuple whose length is not equal to `6`.
        ValueError: If element of `padding` is less than `0`.

    Supported Platforms:
        ``Ascend`` ``CPU``

    Examples:
        >>> input_x = Tensor(np.arange(1 * 2 * 2 * 2 * 3).reshape((1, 2, 2, 2, 3)), mindspore.float16)
        >>> output = ops.avg_pool3d(input_x, kernel_size=2, stride=1)
        >>> print(output)
        [[[[[ 5.  6.]]]
          [[[17. 18.]]]]]
    """
    if not isinstance(input_x, (Tensor, Tensor_)):
        raise TypeError("For avg_pool3d, the input input_x must be tensor")

    if len(input_x.shape) != 5:
        raise ValueError("For avg_pool3d, input must have 5 dim, but got {}.".format(len(input_x.shape)))

    _check_avg_pool3d_padding(padding)

    avg_pool_op = _get_cache_prim(P.AvgPool3D)(kernel_size=kernel_size,
                                               strides=stride,
                                               pad_mode='pad',
                                               pad=padding,
                                               ceil_mode=ceil_mode,
                                               count_include_pad=count_include_pad,
                                               divisor_override=divisor_override)
    return avg_pool_op(input_x)


def adaptive_max_pool2d(input_x, output_size, return_indices=False):
    r"""
    This operator applies a 2D adaptive max pooling to an input signal composed of multiple input planes.
    That is, for any input size, the size of the specified output is H x W.
    The number of output features is equal to the number of input planes.

    The input and output data format can be "NCHW" and "CHW". N is the batch size, C is the number of channels,
    H is the feature height, and W is the feature width.

    .. math::

        \begin{align}
        h_{start} &= floor(i * H_{in} / H_{out})\\
        h_{end} &= ceil((i + 1) * H_{in} / H_{out})\\
        w_{start} &= floor(j * W_{in} / W_{out})\\
        w_{end} &= ceil((j + 1) * W_{in} / W_{out})\\
        Output(i,j) &= {\max Input[h_{start}:h_{end}, w_{start}:w_{end}]}
        \end{align}

    Note:
        Ascend platform only supports float16 type for input_x.

    Args:
        input_x (Tensor): The input of adaptive_max_pool2d, which is a 3D or 4D tensor,
            with float16, float32 or float64 data type.

        output_size (Union[int, tuple]): The target output size is H x W.
            ouput_size can be a tuple, or a single H for H x H, and H and W can be int or None
            which means the output size is the same as the input.

        return_indices (bool): If `return_indices` is True, the indices of max value would be output.
            Default: False.

    Returns:
        Tensor, with the same type as the `input_x`.

        Shape of the output is `input_x_shape[:len(input_x_shape) - len(out_shape)] + out_shape`.

    Raises:
        TypeError: If `output_size` is not int or tuple.
        TypeError: If `input_x` is not a tensor.
        TypeError: If `return_indices` is not a bool.
        TypeError: If dtype of `input_x` is not float16, float32 or float64.
        ValueError: If `output_size` is a tuple and the length of `output_size` is not 2.
        ValueError: If the dimension of `input_x` is not NCHW or CHW.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> # case 1: output_size=(None, 2)
        >>> input_x = Tensor(np.array([[[[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]],
        ...                             [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]],
        ...                             [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]]]), mindspore.float32)
        >>> output = ops.adaptive_max_pool2d(input_x, (None, 2))
        >>> print(output)
        [[[[2. 3.]
           [5. 6.]
           [8. 9.]]
          [[2. 3.]
           [5. 6.]
           [8. 9.]]
          [[2. 3.]
           [5. 6.]
           [8. 9.]]]]
        >>> # case 2: output_size=2
        >>> output = ops.adaptive_max_pool2d(input_x, 2)
        >>> print(output)
        [[[[5. 6.]
           [8. 9.]]
          [[5. 6.]
           [8. 9.]]
          [[5. 6.]
           [8. 9.]]]]
        >>> # case 3: output_size=(1, 2)
        >>> output = ops.adaptive_max_pool2d(input_x, (1, 2))
        >>> print(output)
        [[[[8. 9.]]
          [[8. 9.]]
          [[8. 9.]]]]
    """
    _adaptive_max_pool2d = _get_cache_prim(NN_OPS.AdaptiveMaxPool2D)(output_size, return_indices)
    return _adaptive_max_pool2d(input_x)


def adaptive_max_pool3d(x, output_size, return_indices=False):
    r"""
    Applies a 3D adaptive max pooling over an input signal composed of several input planes.

    The output is of size :math:`(D, H, W)`, for any input size.
    The number of output features is equal to the number of input planes.

    Args:
        x (Tensor): Tensor, with shape :math:`(C, D, H, W)` or :math:`(N, C, D, H, W)`, which support int8, int16,
            int32, int64, uint8, uint16, uint32, uint64, float16, float32 or float64 data type.
        output_size (Union[int, tuple]): The target output size. `ouput_size` can be a tuple :math:`(D, H, W)`,
            or an int D for :math:`(D, D, D)`. :math:`D`, :math:`H` and :math:`W` can be int or None
            which means the output size is the same as that of the input.
        return_indices (bool, optional): If `return_indices` is True, the indices of max value would be output,
            else would not be output. Default: False.

    Returns:
        - **y** (Tensor) - Tensor, with the same number of dims and data type as the `x`.
        - **argmax** (Tensor) - Tensor, the indices of max value, which has the same shape as the
          `y` and it's data type is int32. It will output only when `return_indices` is True.

    Raises:
        TypeError: If `x` is not a Tensor.
        ValueError: If the dimensions number of `x` is not 4 or 5.
        TypeError: If dtype of `x` is not int8, int16, int32, int64, uint8, uint16, uint32, uint64,
                   float16, float32 or float64.
        ValueError: If `output_size` is neither an int nor a tuple with shape (3,).

    Supported Platforms:
        ``GPU`` ``CPU``

    Examples:
        >>> x = Tensor(np.arange(0,36).reshape((1, 3, 3, 4)).astype(np.float32))
        >>> output_size = (1, 1, 2)
        >>> output = ops.adaptive_max_pool3d(x, output_size, True)
        >>> print(output[0].asnumpy())
        [[[[33. 35.]]]]
        >>> print(output[1].asnumpy())
        [[[[33 35]]]]
    """
    adaptive_max_pool3d_ = _get_cache_prim(NN_OPS.AdaptiveMaxPool3D)()
    output_size_ = Tensor(output_size, dtype=mstype.int32)
    out = adaptive_max_pool3d_(x, output_size_)
    output = out if return_indices else out[0]
    return output


def max_unpool1d(x, indices, kernel_size, stride=None, padding=0, output_size=None):
    r"""
    Computes a partial inverse of maxpool1d.

    maxpool1d is not fully invertible, since the non-maximal values are lost.

    max_unpool1d takes the output of maxpool1d as input including the indices of the maximal values
    and computes a partial inverse in which all non-maximal values are set to zero. Typically the input
    is of shape :math:`(N, C, H_{in})` or :math:`(C, H_{in})`, and the output is of shape :math:`(N, C, H_{out}`
    or :math:`(C, H_{out}`. The operation is as follows.

    .. math::
        \begin{array}{ll} \\
        H_{out} = (H{in} - 1) \times stride[0] - 2 \times padding[0] + kernel\_size[0] \\
        \end{array}

    Args:
        x (Tensor): The input Tensor to invert. Tensor of shape :math:`(N, C, H_{in})` or :math:`(C, H_{in})`.
        indices (Tensor): Index of maximum value.
          Tensor of shape must be same with input 'x'.
          Values of indices must belong to :math:`[0, H_{in} - 1]`.
          Data type must be in int32 or int64.
        kernel_size (Union[int, tuple[int]]): The size of kernel used to take the maximum value.
        stride (Union[int, tuple[int]]): The distance of kernel moving,
            If stride is 0, (0) or None, then stride equal to kernel_size. Default: None.
        padding (Union[int, tuple[int]]): The pad value to be filled. Default: 0.
        output_size (tuple[int], optional): The output shape. Default: None.
            If output_size == (), then the shape of output computed by `kernel_size`, `stride` and `padding`.
            If output_size != (), then output_size must be :math:`(N, C, H)` or
            :math:`(C, H)` and output_size must belong to
            :math:`[(N, C, H_{out} - stride[0]), (N, C, H_{out} + stride[0])]`.

    Returns:
        Tensor, with shape :math:`(N, C, H_{out})` or :math:`(C, H_{out})`,
        with the same data type with `x`.

    Raises:
        TypeError: If data type of `x` or `indices` is not supported.
        TypeError: If `kernel_size`, `stride` or `padding` is neither an int nor a tuple.
        ValueError: If numbers in `stride`, `padding` (also support 0 and (0)) or `kernel_size` is not positive.
        ValueError: If the shapes of `x` and `indices` are not equal.
        ValueError: If `x` whose length is not 2 or 3.
        ValueError: If type of `output_size` is not tuple.
        ValueError: If `output_size` whose length is not 0, 2 or 3.
        ValueError: If `output_size` is not close to output size computed by attr `kernel_size`, `stride`, `padding`.

    Supported Platforms:
        ``GPU`` ``CPU``

    Examples:
        >>> x = Tensor(np.array([[2, 4, 6, 8]]).astype(np.float32))
        >>> indices = Tensor(np.array([[1, 3, 5, 7]]).astype(np.int64))
        >>> output = ops.max_unpool1d(x, indices, kernel_size =2, stride=2, padding=0)
        >>> print(output.asnumpy())
        [[0, 2, 0, 4, 0, 6, 0, 8]]
    """
    if stride is None:
        stride = 0
    if output_size is None:
        output_size = ()
    else:
        if not isinstance(output_size, tuple):
            raise ValueError(f"For max_unpool1d, output_size must be tuple, but type {type(output_size)}.")
        if len(output_size) not in [0, 2, 3]:
            raise ValueError(f"For max_unpool1d, length of output_size with tuple must be 0, 2, 3, "
                             f"but got type {len(output_size)}.")
        if len(output_size) == 2:
            output_size = (1,) + output_size + (1,)
        if len(output_size) == 3:
            output_size = (1,) + output_size

    shape = P.Shape()
    x_shape = shape(x)
    indices_shape = shape(indices)
    x_dim = len(x_shape)
    if x_shape != indices_shape:
        raise ValueError(f"For max_unpool1d, the x shape and indices shape must be equal, but got input "
                         f"shape {x_shape} and indices shape {indices_shape}.")
    if x_dim not in (2, 3):
        raise ValueError(f"For max_unpool1d, the x shape must have 2 or 3 dims, but got {x_dim}.")

    max_unpool_2d = _get_cache_prim(MaxUnpool2D)(ksize=(kernel_size, 1), strides=(stride, 1),
                                                 pads=(padding, 0), output_shape=output_size, data_format="NCHW")
    if x_dim == 2:
        x = x.expand_dims(axis=0)
        indices = indices.expand_dims(axis=0)
        x = x.expand_dims(axis=3)
        indices = indices.expand_dims(axis=3)
        out = max_unpool_2d(x, indices)
        out = out.squeeze(-1)
        out = out.squeeze(0)
    else:
        x = x.expand_dims(axis=3)
        indices = indices.expand_dims(axis=3)
        out = max_unpool_2d(x, indices)
        out = out.squeeze(-1)
    return out


def max_unpool2d(x, indices, kernel_size, stride=None, padding=0, output_size=None):
    r"""
    Computes a partial inverse of maxpool2d.

    maxpool2d is not fully invertible, since the non-maximal values are lost.

    max_unpool2d takes the output of maxpool2d as inputs including the indices of the maximal values
    and computes a partial inverse in which all non-maximal values are set to zero. Typically the input
    is of shape :math:`(N, C, H_{in}, W_{in})` or :math:`(C, H_{in}, W_{in})`, and the output is of
    shape :math:`(N, C, H_{out}, W_{out})` or :math:`(C, H_{out}, W_{out})`. The operation is as follows.

    .. math::
        \begin{array}{ll} \\
        H_{out} = (H{in} - 1) \times stride[0] - 2 \times padding[0] + kernel\_size[0] \\
        W_{out} = (W{in} - 1) \times stride[1] - 2 \times padding[1] + kernel\_size[1] \\
        \end{array}

    Args:
        x (Tensor): The input Tensor to invert.
          Tensor of shape :math:`(N, C, H_{in}, W_{in})` or :math:`(C, H_{in}, W_{in})`.
        indices (Tensor): Max values' index represented by the indices.
          Tensor of shape must be same with input 'x'.
          Values of indices must belong to :math:`[0, H_{in} \times W_{in} - 1]`.
          Data type must be in int32 or int64.
        kernel_size (Union[int, tuple[int]]): The size of kernel used to take the maximum value,
            an int number that represents height and width of the kernel, or a tuple
            of two int numbers that represent height and width respectively.
        stride (Union[int, tuple[int]]): The distance of kernel moving, an int number that represents
            the height and width of movement are both stride, or a tuple of two int numbers that
            represent height and width of movement respectively.
            If stride is 0, (0, 0) or None, then stride equal to kernel_size. Default: None.
        padding (Union[int, tuple[int]]): The pad value to be filled. Default: 0. If `padding` is an integer,
            the paddings of height and width are the same, equal to padding. If `padding` is a tuple of two
            integers, the padding of height and width equal to padding[0] and padding[1] correspondingly.
        output_size (tuple[int], optional): The target output size. Default: None.
            If output_size == (), then the shape of output computed by `kernel_size`, `stride` and `padding`.
            If output_size != (), then output_size must be :math:`(N, C, H, W)` and output_size must belong to
            :math:`[(N, C, H_{out} - stride[0], W_{out} - stride[1]),
            (N, C, H_{out} + stride[0], W_{out} + stride[1])]`.

    Returns:
        Tensor, with shape :math:`(N, C, H_{out}, W_{out})` or :math:`(C, H_{out}, W_{out})`,
        with the same data type with `x`.

    Raises:
        TypeError: If data type of `x` or `indices` is not supported.
        TypeError: If `kernel_size`, `stride` or `padding` is neither an int nor a tuple.
        ValueError: If numbers in `stride`, `padding` (also support 0 and (0, 0)) or `kernel_size` is not positive.
        ValueError: If the shape of `x` and `indices` are not equal.
        ValueError: If `kernel_size`, `stride` or `padding` is a tuple whose length is not equal to 2.
        ValueError: If `x` whose length is not 3 or 4.
        ValueError: If `output_size` whose type is not tuple.
        ValueError: If `output_size` whose length is not 0, 3 or 4.
        ValueError: If `output_size` is not close to output size computed by attr `kernel_size`, `stride`, `padding`.

    Supported Platforms:
        ``GPU`` ``CPU``

    Examples:
        >>> x = Tensor(np.array([[[[0, 1], [8, 9]]]]).astype(np.float32))
        >>> indices = Tensor(np.array([[[[0, 1], [2, 3]]]]).astype(np.int64))
        >>> output = ops.max_unpool2d(x, indices, kernel_size=1, stride=1, padding=0)
        >>> print(output.asnumpy())
        [[[[0. 1.]
           [8. 9.]]]]
    """
    if stride is None:
        stride = 0
    if output_size is None:
        output_size = ()
    else:
        if not isinstance(output_size, tuple):
            raise ValueError(f"For max_unpool2d, output_size must be tuple, but type {type(output_size)}.")
        if len(output_size) not in [0, 3, 4]:
            raise ValueError(f"For max_unpool2d, length of output_size with tuple must be 0, 3, 4, "
                             f"but got type {len(output_size)}.")
        if len(output_size) == 3:
            output_size = (1,) + output_size

    shape = P.Shape()
    x_shape = shape(x)
    indices_shape = shape(indices)
    x_dim = len(x_shape)
    if x_shape != indices_shape:
        raise ValueError(f"For max_unpool2d, the x shape and indices shape must be equal, but got input "
                         f"shape {x_shape} and indices shape {indices_shape}.")
    if x_dim not in (3, 4):
        raise ValueError(f"For max_unpool2d, the x shape must have 3 or 4 dims, but got {x_dim}.")

    max_unpool_2d = MaxUnpool2D(ksize=kernel_size, strides=stride, pads=padding, output_shape=output_size,
                                data_format="NCHW")
    if x_dim == 3:
        x = x.expand_dims(axis=0)
        indices = indices.expand_dims(axis=0)
        out = max_unpool_2d(x, indices)
        out = out.squeeze(0)
    else:
        out = max_unpool_2d(x, indices)
    return out


def max_unpool3d(x, indices, kernel_size, stride=None, padding=0, output_size=None):
    r"""
    Computes a partial inverse of maxpool3d.

    maxpool3d is not fully invertible, since the non-maximal values are lost.

    max_unpool3d takes the output of maxpool3d as input including the indices of the maximal values and computes a
    partial inverse in which all non-maximal values are set to zero. Typically the input is of shape
    :math:`(N, C, D_{in}, H_{in}, W_{in})` or :math:`(C, D_{in}, H_{in}, W_{in})`, and the output is of shape
    :math:`(N, C, D_{out}, H_{out}, W_{out})` or :math:`(C, D_{out}, H_{out}, W_{out})`. The operation is as follows.

    .. math::
        \begin{array}{ll} \\
        D_{out} = (D{in} - 1) \times stride[0] - 2 \times padding[0] + kernel\_size[0] \\
        H_{out} = (H{in} - 1) \times stride[1] - 2 \times padding[1] + kernel\_size[1] \\
        W_{out} = (W{in} - 1) \times stride[2] - 2 \times padding[2] + kernel\_size[2] \\
        \end{array}

    Args:
        x (Tensor): The input Tensor to invert.
          Tensor of shape :math:`(N, C, D_{in}, H_{in}, W_{in})` or :math:`(C, D_{in}, H_{in}, W_{in})`.
        indices (Tensor): Max values' index represented by the indices. Tensor of shape must be same with input 'x'.
          Values of indices must belong to :math:`[0, D_{in} \times H_{in} \times W_{in} - 1]`.
          Data type must be in int32 or int64.
        kernel_size (Union[int, tuple[int]]): The size of kernel used to take the maximum value,
            an int number that represents depth, height and width of the kernel, or a tuple
            of three int numbers that represent depth, height and width respectively.
        stride (Union[int, tuple[int]]): The distance of kernel moving, an int number that represents
            the depth, height and width of movement are both stride, or a tuple of three int numbers that
            represent depth, height and width of movement respectively.
            If stride is 0, (0, 0, 0) or None, then stride equal to kernel_size. Default: None.
        padding (Union[int, tuple[int]]): The pad value to be filled. Default: 0. If `padding` is an integer,
            the paddings of depth, height and width are the same, equal to padding. If `padding` is a tuple of three
            integers, the padding of depth, height and width equal to padding[0], padding[1] and padding[2]
            correspondingly.
        output_size (tuple[int], optional): The output size. Default: None. If output_size == (), then the shape of
            output computed by `kernel_size`, `stride` and `padding`. If output_size != (), then output_size must be
            :math:`(N, C, D, H, W)` or :math:`(C, D, H, W)` and output_size must belong to
            :math:`[(N, C, D_{out} - stride[0], H_{out} - stride[1], W_{out} - stride[2]),
            (N, C, D_{out} + stride[0], H_{out} + stride[1], W_{out} + stride[2])]`.

    Returns:
        Tensor, with shape :math:`(N, C, D_{out}, H_{out}, W_{out})` or :math:`(C, D_{out}, H_{out}, W_{out})`,
        with the same data type with `x`.

    Raises:
        TypeError: If data type of `x` or `indices` is not supported.
        TypeError: If `kernel_size`, `stride` or `padding` is neither an int nor a tuple.
        ValueError: If numbers in `stride` or `padding` (also support 0 and (0, 0, 0)) or `kernel_size` is not positive.
        ValueError: If the shape of `x` and `indices` are not equal.
        ValueError: If `kernel_size`, `stride` or `padding` is a tuple whose length is not equal to 3.
        ValueError: If `x` whose length is not 4 or 5.
        ValueError: If `output_size` whose length is not 0, 4 or 5.
        ValueError: If `output_size` whose type is not tuple.
        ValueError: If `output_size` is not close to output size computed by attr `kernel_size`, `stride`, `padding`.

    Supported Platforms:
        ``GPU`` ``CPU``

    Examples:
        >>> x = Tensor(np.array([[[[[0, 1], [8, 9]]]]]).astype(np.float32))
        >>> indices= Tensor(np.array([[[[[0, 1], [2, 3]]]]]).astype(np.int64))
        >>> output = ops.max_unpool3d(x, indices, kernel_size=2, stride=1, padding=0)
        >>> print(output)
        [[[[[0. 1. 8.]
            [9. 0. 0.]
            [0. 0. 0.]]
           [[0. 0. 0.]
            [0. 0. 0.]
            [0. 0. 0.]]]]]
    """
    if stride is None:
        stride = 0
    if output_size is None:
        output_size = ()
    else:
        if not isinstance(output_size, tuple):
            raise ValueError(f"For max_unpool3d, output_size must be tuple, but type {type(output_size)}.")
        if len(output_size) not in [0, 4, 5]:
            raise ValueError(f"For max_unpool3d, length of output_size with tuple must be 0, 4, 5, "
                             f"but got type {len(output_size)}.")
        if len(output_size) == 4:
            output_size = (1,) + output_size
    max_unpool_3d = MaxUnpool3D(ksize=kernel_size, strides=stride, pads=padding, output_shape=output_size,
                                data_format="NCDHW")
    shape = P.Shape()
    x_shape = shape(x)
    indices_shape = shape(indices)
    x_dim = len(x_shape)
    if x_shape != indices_shape:
        raise ValueError(f"For max_unpool3d, the x shape and indices shape must be equal, but got input "
                         f"shape {x_shape} and indices shape {indices_shape}.")
    if x_dim not in (4, 5):
        raise ValueError(f"For max_unpool3d, the x shape must have 4 or 5 dims, but got {x_dim}.")
    if x_dim == 4:
        x = x.expand_dims(axis=0)
        indices = indices.expand_dims(axis=0)
        out = max_unpool_3d(x, indices)
        out = out.squeeze(0)
    else:
        out = max_unpool_3d(x, indices)
    return out


def binary_cross_entropy_with_logits(logits, label, weight, pos_weight, reduction='mean'):
    r"""
    Adds sigmoid activation function to input `logits`, and uses the given logits to compute binary cross entropy
    between the logits and the label.

    Sets input logits as :math:`X`, input label as :math:`Y`, input weight as :math:`W`, output as :math:`L`. Then,

    .. math::

        \begin{array}{ll} \\
            p_{ij} = sigmoid(X_{ij}) = \frac{1}{1 + e^{-X_{ij}}} \\
            L_{ij} = -[Y_{ij} * log(p_{ij}) + (1 - Y_{ij})log(1 - p_{ij})]
        \end{array}

    :math:`i` indicates the :math:`i^{th}` sample, :math:`j` indicates the category. Then,

    .. math::
        \ell(x, y) = \begin{cases}
        L, & \text{if reduction} = \text{'none';}\\
        \operatorname{mean}(L), & \text{if reduction} = \text{'mean';}\\
        \operatorname{sum}(L),  & \text{if reduction} = \text{'sum'.}
        \end{cases}

    :math:`\ell` indicates the method of calculating the loss. There are three methods:
    the first method is to provide the loss value directly,
    the second method is to calculate the average value of all losses,
    and the third method is to calculate the sum of all losses.

    This operator will multiply the output by the corresponding weight.
    The tensor weight assigns different weights to each piece of data in the batch,
    and the tensor pos_weight adds corresponding weights to the positive examples of each category.

    In addition, it can trade off recall and precision by adding weights to positive examples.
    In the case of multi-label classification the loss can be described as:

    .. math::
        \begin{array}{ll} \\
            p_{ij,c} = sigmoid(X_{ij,c}) = \frac{1}{1 + e^{-X_{ij,c}}} \\
            L_{ij,c} = -[P_{c}Y_{ij,c} * log(p_{ij,c}) + (1 - Y_{ij,c})log(1 - p_{ij,c})]
        \end{array}

    where c is the class number (c>1 for multi-label binary classification, c=1 for single-label binary classification),
    n is the number of the sample in the batch and :math:`p_c` is the weight of the positive answer for the class c.
    :math:`p_c>1` increases the recall, :math:`p_c<1` increases the precision.

    Args:
        logits (Tensor): Input logits. Data type must be float16 or float32.
          Tensor of shape :math:`(N, *)` where :math:`*` means, any number of additional dimensions.
        label (Tensor): Ground truth label, has the same shape as `logits`.
          Data type must be float16 or float32.
        weight (Tensor): A rescaling weight applied to the loss of each batch element. It can be
          broadcast to a tensor with shape of `logits`. Data type must be float16 or float32.
        pos_weight (Tensor): A weight of positive examples. Must be a vector with length equal to the
          number of classes. It can be broadcast to a tensor with shape of `logits`.
          Data type must be float16 or float32.
        reduction (str): Type of reduction to be applied to loss. The optional values are 'mean', 'sum', and 'none',
             not case sensitive. If 'none', do not perform reduction. Default: 'mean'.
    Returns:
        Tensor or Scalar, if `reduction` is 'none', it's a tensor with the same shape and type as input `logits`.
        Otherwise, the output is a scalar.

    Raises:
        TypeError: If input `logits`, `label`, `weight`, `pos_weight` is not Tensor.
        TypeError: If data type of input `logits`, `label`, `weight`, `pos_weight` is neither float16 nor float32.
        TypeError: If data type of input `reduction` is not string.
        ValueError: If `weight` or `pos_weight` can not be broadcast to a tensor with shape of `logits`.
        ValueError: If `reduction` is not one of 'none', 'mean' or 'sum'.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> logits = Tensor(np.array([[-0.8, 1.2, 0.7], [-0.1, -0.4, 0.7]]), mindspore.float32)
        >>> label = Tensor(np.array([[0.3, 0.8, 1.2], [-0.6, 0.1, 2.2]]), mindspore.float32)
        >>> weight = Tensor(np.array([1.0, 1.0, 1.0]), mindspore.float32)
        >>> pos_weight = Tensor(np.array([1.0, 1.0, 1.0]), mindspore.float32)
        >>> output = ops.binary_cross_entropy_with_logits(logits, label, weight, pos_weight)
        >>> print(output)
        0.3463612
    """

    bce_with_logits_loss_op = _get_cache_prim(NN_OPS.BCEWithLogitsLoss)(reduction)
    return bce_with_logits_loss_op(logits, label, weight, pos_weight)


def dropout(x, p=0.5, seed0=0, seed1=0):
    """
    During training, randomly zeroes some of the elements of the input tensor
    with probability `p` from a Bernoulli distribution. It plays the role of
    reducing neuron correlation and avoid overfitting.

    Args:
        x (Tensor): The input of Dropout, a Tensor of any shape with data type of float16 or float32.
        p (float, optional): The dropping rate, between 0 and 1, e.g. p = 0.1,
            means dropping out 10% of input units. Default: 0.5.
        seed0 (int, optional): seed0 value for random generating. Default: 0.
        seed1 (int, optional): seed1 value for random generating. Default: 0.

    Returns:
        - **output** (Tensor) - With the same shape and data type as `x`.
        - **mask** (Tensor) - With the same shape as `x`.

    Raises:
        TypeError: If `p` is not a float.
        TypeError: If `seed0` or `seed1` is not an int.
        TypeError: If dtype of `x` is neither float16 nor float32.
        TypeError: If `x` is not a Tensor.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> x = Tensor(((20, 16), (50, 50)), mindspore.float32)
        >>> output, mask = ops.dropout(x, p=0.5)
        >>> print(output.shape)
        (2, 2)
    """
    keep_prob = 1 - p
    dropout_ = P.Dropout(keep_prob=keep_prob, Seed0=seed0, Seed1=seed1)
    return dropout_(x)


def celu(x, alpha=1.0):
    r"""
    celu activation function, computes celu (Continuously differentiable exponential
    linear units) of input tensors element-wise. The formula is defined as follows:

    .. math::

        \text{CeLU}(x) = \max(0,x) + \min(0, \alpha * (\exp(x/\alpha) - 1))

    For more details, please refer to `celu <https://arxiv.org/abs/1704.07483>`_.

    Args:
        x (Tensor): The input of celu with data type of float16 or float32.
        alpha (float): The :math:`\alpha` value for the Celu formulation. Default: 1.0

    Returns:
        Tensor, has the same data type and shape as the input.

    Raises:
        TypeError: If `alpha` is not a float.
        TypeError: If `x` is not a Tensor.
        TypeError: If dtype of `x` is neither float16 nor float32.
        ValueError: If `alpha` has the value of 0.

    Supported Platforms:
        ``Ascend`` ``CPU`` ``GPU``

    Examples:
        >>> x = Tensor(np.array([-2.0, -1.0, 1.0, 2.0]), mindspore.float32)
        >>> output = ops.celu(x, alpha=1.0)
        >>> print(output)
        [-0.86466473 -0.63212055  1.          2.        ]
    """
    celu_op = _get_cache_prim(P.CeLU)(alpha)
    return celu_op(x)


def dropout1d(x, p=0.5, training=True):
    r"""
    During training, randomly zeroes some channels of the input tensor with probability `p`
    from a Bernoulli distribution(For a 3-dimensional tensor with a shape of :math:`NCL`,
    the channel feature map refers to a 1-dimensional feature map with the shape of :math:`L`).

    For example, the :math:`j\_th` channel of the :math:`i\_th` sample in the batched input is a to-be-processed
    `1D` tensor input[i,j].
    Each channel will be zeroed out independently on every forward call which based on Bernoulli distribution
    probability `p`.

    The parper `Dropout: A Simple Way to Prevent Neural Networks from Overfitting
    <http://www.cs.toronto.edu/~rsalakhu/papers/srivastava14a.pdf>`_ mentioned this technology，And it is proved that
    it can effectively reduce over fitting and prevent neuronal coadaptation.
    For more details, refer to `Improving neural networks by preventing co-adaptation of feature detectors
    <https://arxiv.org/pdf/1207.0580.pdf>`_ .

    `dropout1d` can improve the independence between channel feature maps.

    Args:
        x (Tensor): A tensor with shape :math:`(N, C, L)` or :math:`(C, L)`, where `N` is the batch size, `C` is the
            number of channels, `L` is the feature length. The data type must be int8, int16, int32, int64, float16,
            float32 or float64.
        p (float): The dropping probability of a channel, between 0 and 1, e.g. `p` = 0.8,
            which means an 80% chance of clearing. Default: 0.5.
        training (bool): Apply dropout if is True. Default: True.

    Returns:
        Tensor, output, with the same shape and data type as `x`.

    Raises:
        TypeError: If `x` is not a Tensor.
        TypeError: If dtype of `x` is not int8, int16, int32, int64, float16, float32 or float64.
        TypeError: If the data type of `p` is not float.
        ValueError: If `p` is out of the range `[0.0, 1.0]`.
        ValueError: If `x` shape is not `2D` or `3D`.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> input_x = Tensor(np.random.randn(4, 3), mindspore.float32)
        >>> output = ops.dropout1d(input_x, 0.5)
        >>> print(output.shape)
        (4, 3)
    """
    if not training:
        p = 0
    dropout_2d_op = NN_OPS.Dropout2D(1.0 - p)

    if len(x.shape) == 2:
        x = x.expand_dims(0)
        x = x.expand_dims(-1)
        out, _ = dropout_2d_op(x)
        out = out.squeeze(-1)
        out = out.squeeze(0)
    else:
        x = x.expand_dims(-1)
        out, _ = dropout_2d_op(x)
        out = out.squeeze(-1)
    return out


def dropout2d(x, p=0.5):
    r"""
    During training, randomly zeroes some channels of the input tensor with probability `p`
    from a Bernoulli distribution(For a 4-dimensional tensor with a shape of :math:`NCHW`,
    the channel feature map refers to a 2-dimensional feature map with the shape of :math:`HW`).

    For example, the :math:`j\_th` channel of the :math:`i\_th` sample in the batched input is a to-be-processed
    `2D` tensor input[i,j].
    Each channel will be zeroed out independently on every forward call which based on Bernoulli distribution
    probability `p`.
    The parper `Dropout: A Simple Way to Prevent Neural Networks from Overfitting
    <http://www.cs.toronto.edu/~rsalakhu/papers/srivastava14a.pdf>`_ mentioned this technology，And it is proved that
    it can effectively reduce over fitting and prevent neuronal coadaptation.
    For more details, refer to `Improving neural networks by preventing co-adaptation of feature detectors
    <https://arxiv.org/pdf/1207.0580.pdf>`_ .

    `dropout2d` can improve the independence between channel feature maps.

    Args:
        x (Tensor): A `4D` tensor with shape :math:`(N, C, H, W)`, where `N` is the batch size, `C` is the number
            of channels, `H` is the feature height, and `W` is the feature width. The data type must be int8,
            int16, int32, int64, float16, float32 or float64.
        p (float): The dropping probability of a channel, between 0 and 1, e.g. `p` = 0.8,
            which means dropping out 80% of channels. Default: 0.5.

    Returns:
        Tensor, output, with the same shape and data type as `x`.

        Tensor, mask, with the same shape as `x` and the data type is bool.

    Raises:
        TypeError: If `x` is not a Tensor.
        TypeError: If dtype of `x` is not int8, int16, int32, int64, float16, float32 or float64.
        TypeError: If the data type of `p` is not float.
        ValueError: If `p` is out of the range `[0.0, 1.0]`.
        ValueError: If `x` shape is not `4D`.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> input_x = Tensor(np.ones([2, 1, 2, 3]), mindspore.float32)
        >>> output, mask = ops.dropout2d(input_x, 0.5)
        >>> print(output.shape)
        (2, 1, 2, 3)
    """
    dropout_2d_op = NN_OPS.Dropout2D(1.0 - p)
    return dropout_2d_op(x)


def dropout3d(x, p=0.5):
    r"""
    During training, randomly zeroes some channels of the input tensor
    with probability `p` from a Bernoulli distribution(For a 5-dimensional tensor
    with a shape of :math:`NCDHW`, the channel feature map refers to a 3-dimensional
    feature map with a shape of :math:`DHW`).

    For example, the :math:`j\_th` channel of the :math:`i\_th` sample in the batched input is a to-be-processed
    `3D` tensor input[i,j].
    Each channel will be zeroed out independently on every forward call which based on Bernoulli distribution
    probability `p`.

    `dropout3d` can improve the independence between channel feature maps.

    Args:
        x (Tensor): A `5D` tensor with shape :math:`(N, C, D, H, W)`, where `N` is the batch size, `C` is the number
            of channels, `D` is the feature depth, `H` is the feature height, and `W` is the feature width.
            The data type must be int8, int16, int32, int64, float16, float32 or float64.
        p (float): The dropping probability of a channel, between 0 and 1, e.g. `p` = 0.8,
            which means dropping out 80% of channels. Default: 0.5.

    Returns:
        Tensor, output, with the same shape and data type as `x`.

        Tensor, mask, with the same shape as `x` and the data type is bool.

    Raises:
        TypeError: If `x` is not a Tensor.
        TypeError: If dtype of `x` is not int8, int16, int32, int64, float16, float32 or float64.
        TypeError: If the data type of `p` is not float.
        ValueError: If `p` is out of the range `[0.0, 1.0]`.
        ValueError: If `x` shape is not 5D.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> input_x = Tensor(np.ones([2, 1, 2, 1, 2]), mindspore.float32)
        >>> output, mask = ops.dropout3d(input_x, 0.5)
        >>> print(output.shape)
        (2, 1, 2, 1, 2)
    """
    dropout_3d_op = NN_OPS.Dropout3D(1.0 - p)
    return dropout_3d_op(x)


def fast_gelu(x):
    r"""
    Fast Gaussian Error Linear Units activation function.

    FastGeLU is defined as follows:

    .. math::
        \text{output} = \frac {x} {1 + \exp(-1.702 * \left| x \right|)} * \exp(0.851 * (x - \left| x \right|)),

    where :math:`x` is the element of the input.

    Args:
        x (Tensor): Input to compute the FastGeLU with data type of float16 or float32.

    Returns:
        Tensor, with the same type and shape as `x`.

    Raises:
        TypeError: If dtype of `x` is neither float16 nor float32.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> x = Tensor(np.array([[-1.0, 4.0, -8.0], [2.0, -5.0, 9.0]]), mindspore.float32)
        >>> output = ops.fast_gelu(x)
        >>> print(output)
        [[-1.5418735e-01  3.9921875e+00 -9.7473649e-06]
         [ 1.9375000e+00 -1.0052517e-03  8.9824219e+00]]
    """
    return fast_gelu_(x)


@constexpr
def _check_float_range_inc_right(arg_value, lower_limit, upper_limit, arg_name=None, prim_name=None):
    """
    Method for checking whether input value is in float range inc right.
    """
    return validator.check_float_range(arg_value, lower_limit, upper_limit, Rel.INC_RIGHT, arg_name, prim_name)


def fractional_max_pool2d(input_x, kernel_size, output_size=None, output_ratio=None, return_indices=False,
                          _random_samples=None):
    r"""
    Applies a 2D fractional max pooling to an input signal.
    The input is composed of multiple input planes.
    The max-pooling operation is applied in kH × kW regions by a stochastic step size determined by
    the target output size. For any input size, the size of the specified output is H x W. The number
    of output features is equal to the number of input planes.

    Fractional MaxPooling is described in the paper `Fractional Max-Pooling <https://arxiv.org/pdf/1412.6071>`_.

    Args:
        input_x (Tensor): Tensor of shape :math:`(N, C, H_{in}, W_{in})`,
            with float16, float32, float64, int32, int64 data type.
        kernel_size (Union[int, tuple[int]]): The size of kernel used to take the maximum value,
            is an int number that represents height and width of the kernel, or a tuple
            of two int numbers that represent height and width respectively.
            The value must be a positive integer.
        output_size (Union[int, tuple[int]], optional): The shape of the target `output_size`,
            is an int number that represents height and width, or a tuple
            of two int numbers that represent height and width respectively.
            The value must be a positive integer.
            Default: None.
        output_ratio (Union[float, tuple[float]], optional): The ratio of target output shape to input shape.
            Specifying the size of the output tensor by using a ratio of the input size.
            Data type: float16, float32, double, and value is between (0, 1).
            Default: None.
        return_indices (bool, optional): If `return_indices` is True, the indices of max value would be output.
            Default: False.
        _random_samples (Tensor, optional): The random step of FractionalMaxPool2d, which is a 3D tensor.
            Tensor of data type: float16, float32, double, and value is between (0, 1).
            Supported shape :math:`(N, C, 2)`.
            Default: None.

    Returns:
        - **y** (Tensor) - Has the same type as the `input_x`.
          Has the shape :math:`(N, C, H, W)`.

        - **argmax** (Tensor) - The indices along with the outputs, which is a Tensor, with the same shape as the
          `y` and int64 data type. It will output only when `return_indices` is True.

    Raises:
        TypeError: If data type of `input_x` is not one of the following: float16, float32, float64, int32, int64.
        TypeError: If data type of `_random_samples` is not one of the following: float16, float32, float64.
        ValueError: If `kernel_size` is not a number and `kernel_size` is not a tuple of length 2.
        ValueError: If `output_size` is not a number and `output_size` is not a tuple of length 2.
        ValueError: If the sum of `kernel_size` , `output_size` and -1 is larger than the corresponding
                    dimension of `input_x`.
        ValueError: If the dimension of `_random_samples` is not 3.
        ValueError: if `output_size` and `output_ratio` are None at the same time.
        ValueError: If the first dimension size of `input_x` and `_random_samples` is not equal.
        ValueError: If the second dimension size of `input_x` and `_random_samples` is not equal.
        ValueError: If the third dimension size of `_random_samples` is not 2.

    Supported Platforms:
        ``CPU``

    Examples:
        >>> input_x = Tensor(np.array([0.3220, 0.9545, 0.7879, 0.0975, 0.3698,
        ...                            0.5135, 0.5740, 0.3435, 0.1895, 0.8764,
        ...                            0.9581, 0.4760, 0.9014, 0.8522, 0.3664,
        ...                            0.4980, 0.9673, 0.9879, 0.6988, 0.9022,
        ...                            0.9304, 0.1558, 0.0153, 0.1559, 0.9852]).reshape([1, 1, 5, 5]), mstype.float32)
        >>> _random_samples = Tensor(np.array([[[0.8, 0.8]]]), mstype.float32)
        >>> y, argmax = ops.fractional_max_pool2d(input_x, kernel_size=2, output_size=(2, 2),
        ...                                       _random_samples=_random_samples, return_indices=True)
        >>> print(y)
        [[[[0.9545 0.8764]
           [0.9673 0.9852]]]]
        >>> print(argmax)
        [[[[ 1  9]
           [16 24]]]]
        >>> y, argmax = ops.fractional_max_pool2d(input_x, kernel_size=2, output_ratio=(0.5, 0.5),
        ...                                       _random_samples=_random_samples, return_indices=True)
        >>> print(y)
        [[[[0.9545 0.8764]
           [0.9673 0.9852]]]]
        >>> print(argmax)
        [[[[ 1  9]
           [16 24]]]]
    """
    if output_ratio is not None and output_size is not None or output_ratio is None and output_size is None:
        raise ValueError(f"For fractional_max_pool2d, 'output_size' and 'output_ratio' can not be specified or None"
                         f"at the same time, but got {output_ratio} and {output_size} .")
    if len(input_x.shape) == 3:
        input_x.expend_dims(axis=0)
    if _random_samples is None:
        _random_samples = Tensor([[[0, 0]]], mstype.float32)
    if output_ratio is not None:
        if isinstance(output_ratio, float):
            output_ratio = (output_ratio, output_ratio)
        _check_float_range_inc_right(output_ratio[0], 0.0, 1.0)
        _check_float_range_inc_right(output_ratio[1], 0.0, 1.0)
        output_size = (int(input_x.shape[-2] * output_ratio[0]), int(input_x.shape[-1] * output_ratio[1]))
    fractional_max_pool = FractionalMaxPoolWithFixedKsize(kernel_size, output_size)
    output = fractional_max_pool(input_x, _random_samples)
    if return_indices:
        return output
    return output[0]


def fractional_max_pool3d(input_x, kernel_size, output_size=None, output_ratio=None, return_indices=False,
                          _random_samples=None):
    r"""
    This operator applies a 3D fractional max pooling over an input signal.
    The input is composed of several input planes.
    The max-pooling operation is applied in kD x kH x kW regions by a stochastic step size determined
    by the target output size.The number of output features is equal to the number of input planes.

    Refer to the paper `Fractional MaxPooling by Ben Graham <https://arxiv.org/abs/1412.6071>`_  for more details.

    The input and output data format can be "NCDHW". N is the batch size, C is the number of channels,
    D the feature depth, H is the feature height, and W is the feature width.

    Args:
        input_x (Tensor): The input of FractionalMaxPool3d, which is a 4D or 5D tensor.
            Tensor of data type: float16, float32, double, int32, int64.
            Supported shape :math:`(N, C, D_{in}, H_{in}, W_{in})`.
        kernel_size (Union[int, tuple[int]]): The size of kernel used to take the maximum value,
            is an int number that represents depth, height and width of the kernel, or a tuple
            of three int numbers that represent depth, height and width respectively.
            The value must be a positive integer.
        output_size (Union[int, tuple[int]], optional): The Shape of the target `output_size`,
            is an int number that represents depth, height and width, or a tuple
            of three int numbers that represent depth, height and width respectively.
            The value must be a positive integer.
            Default: None.
        output_ratio (Union[float, tuple[float]], optional): The ratio of target output shape to input shape.
            Specifying the size of the output tensor by using a ratio of the input size.
            Data type: float16, float32, double, and value is between (0, 1).
            Default: None.
        return_indices (bool, optional): If `return_indices` is True, the indices of max value would be output.
            Default: False.
        _random_samples (Tensor, optional): The random step of FractionalMaxPool3d, which is a 3D tensor.
            Tensor of data type: float16, float32, double, and value is between (0, 1).
            Supported shape :math:`(N, C, 3)`.

    Returns:
        - **y** (Tensor) - A tensor, the output of FractionalMaxPool3d.
          Has the same data type with `imput_x`.
          Tensor of shape :math:`(N, C, D, H, W)` .

        - **argmax** (Tensor) - The indices along with the outputs, which is a Tensor, with the same shape as the
          `y` and int32 data type. It will output only when `return_indices` is True.

    Raises:
        TypeError: If `input_x` is not a 4D or 5D tensor.
        TypeError: If `_random_samples` is not a 3D tensor.
        TypeError: If data type of `imput_x` is not float16, float32, double, int32, int64.
        TypeError: If dtype of `_random_samples` is not float16, float32, double.
        TypeError: If dtype of `argmax` is not int32, int64.
        ValueError: If `output_size` is a tuple and if `output_size` length is not 3.
        ValueError: If `kernel_size` is a tuple and if `kernel_size` length is not 3.
        ValueError: If numbers in `output_size` or `kernel_size` is not positive.
        ValueError: if `output_size` and `output_ratio` are None at the same time.
        ValueError: If the first dimension size of `input_x` and `_random_samples` is not equal.
        ValueError: If the second dimension size of `input_x` and `_random_samples` is not equal.
        ValueError: If the third dimension size of `_random_samples` is not 3.

    Supported Platforms:
        ``GPU`` ``CPU``

    Examples:
        >>> x = Tensor(np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
        ...            .reshape([1, 1, 2, 2, 4]), mstype.float32)
        >>> _random_samples = Tensor(np.array([0.7, 0.7, 0.7]).reshape([1, 1, 3]), mstype.float32)
        >>> output, argmax = ops.fractional_max_pool3d(x, kernel_size=(1.0, 1.0, 1.0), output_size=(1, 1, 3),
        ...                                            _random_samples=_random_samples, return_indices=True)
        >>> print(output)
        [[[[[13. 14. 16.]]]]]
        >>> print(argmax)
        [[[[[12 13 15]]]]]
        >>> output, argmax = ops.fractional_max_pool3d(x, kernel_size=(1.0, 1.0, 1.0), output_ratio=(0.5, 0.5, 0.5),
        ...                                            _random_samples=_random_samples, return_indices=True)
        >>> print(output)
        [[[[[13. 16.]]]]]
        >>> print(argmax)
        [[[[[12 15]]]]]
    """
    if output_ratio is not None and output_size is not None or output_ratio is None and output_size is None:
        raise ValueError(f"For fractional_max_pool2d, 'output_size' and 'output_ratio' can not be specified or None"
                         f"at the same time, but got {output_ratio} and {output_size} .")
    if len(input_x.shape) == 4:
        input_x.expend_dims(axis=0)
    if _random_samples is None:
        _random_samples = Tensor([[[0, 0, 0]]], mstype.float32)
    if output_ratio is not None:
        if isinstance(output_ratio, float):
            output_ratio = (output_ratio, output_ratio, output_ratio)
        _check_float_range_inc_right(output_ratio[0], 0.0, 1.0)
        _check_float_range_inc_right(output_ratio[1], 0.0, 1.0)
        _check_float_range_inc_right(output_ratio[2], 0.0, 1.0)
        output_size = (int(input_x.shape[-3] * output_ratio[0]), int(input_x.shape[-2] * output_ratio[1]),
                       int(input_x.shape[-1] * output_ratio[2]))
    fractional_max_pool = FractionalMaxPool3DWithFixedKsize(kernel_size, output_size)
    output = fractional_max_pool(input_x, _random_samples)
    if return_indices:
        return output
    return output[0]


def kl_div(logits, labels, reduction='mean'):
    r"""
    Computes the Kullback-Leibler divergence between the logits and the labels.

    The updating formulas of KLDivLoss algorithm are as follows,

    .. math::
        L = \{l_1,\dots,l_N\}^\top, \quad
        l_n = target_n \cdot (\log target_n - x_n)

    Then,

    .. math::
        \ell(x, target) = \begin{cases}
        L, & \text{if reduction} = \text{'none';}\\
        \operatorname{mean}(L), & \text{if reduction} = \text{'mean';}\\
        \operatorname{batchmean}(L), & \text{if reduction} = \text{'batchmean';}\\
        \operatorname{sum}(L),  & \text{if reduction} = \text{'sum'.}
        \end{cases}

    where :math:`x` represents `logits`.
    :math:`target` represents `labels`.
    :math:`\ell(x, target)` represents `output`.

    Note:
        - Currently it does not support float64 input on `Ascend`.
        - The output aligns with the mathematical definition of Kullback-Leibler divergence
          only when `reduction` is set to 'batchmean'.

    Args:
        logits (Tensor): The input Tensor. The data type must be float16, float32 or float64.
        labels (Tensor): The label Tensor which has the same shape and data type as `logits`.
        reduction (str): Specifies the reduction to be applied to the output.
            Its value must be one of 'none', 'mean', 'batchmean' or 'sum'. Default: 'mean'.

    Returns:
        Tensor or Scalar, if `reduction` is 'none', then output is a tensor and has the same shape as `logits`.
        Otherwise, it is a scalar.

    Raises:
        TypeError: If `reduction` is not a str.
        TypeError: If neither `logits` nor `labels` is a Tensor.
        TypeError: If dtype of `logits` or `labels` is not float32.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> logits = Tensor(np.array([0.2, 0.7, 0.1]), mindspore.float32)
        >>> labels = Tensor(np.array([0., 1., 0.]), mindspore.float32)
        >>> output = mindspore.ops.kl_div(logits, labels, 'mean')
        >>> print(output)
        -0.23333333
    """
    if not isinstance(reduction, str):
        raise ValueError("For 'kl_div', the 'reduction' must be str and must be in "
                         f"'['none', 'mean', 'batchmean', 'sum']', but got '{reduction}'.")

    if reduction == 'batchmean':
        kl_div_sum = P.KLDivLoss(reduction='sum')(logits, labels)
        shape = P.TensorShape()(logits)
        batch_size = shape[0]
        return kl_div_sum / batch_size

    if reduction == 'mean':
        kl_div_sum = P.KLDivLoss(reduction='sum')(logits, labels)
        shape = P.TensorShape()(logits)
        total_size = 1
        for dim in shape:
            total_size = total_size * dim
        return kl_div_sum / total_size

    return P.KLDivLoss(reduction=reduction)(logits, labels)


def hardshrink(x, lambd=0.5):
    r"""
    Hard Shrink activation function. Calculates the output according to the input elements.

    The formula is defined as follows:

    .. math::
        \text{HardShrink}(x) =
        \begin{cases}
        x, & \text{ if } x > \lambda \\
        x, & \text{ if } x < -\lambda \\
        0, & \text{ otherwise }
        \end{cases}

    Args:
        x (Tensor): The input of Hard Shrink with data type of float16 or float32.
        lambd (float): The threshold :math:`\lambda` defined by the Hard Shrink formula. Default: 0.5.

    Returns:
        Tensor, has the same data type and shape as the input `x`.

    Raises:
        TypeError: If `lambd` is not a float.
        TypeError: If `x` is not a tensor.
        TypeError: If dtype of `x` is neither float16 nor float32.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> x = Tensor(np.array([[ 0.5,  1,  2.0], [0.0533,0.0776,-2.1233]]), mindspore.float32)
        >>> output = ops.hardshrink(x)
        >>> print(output)
        [[ 0.      1.      2.    ]
        [ 0.      0.     -2.1233]]
    """
    hshrink_op = _get_cache_prim(P.HShrink)(lambd)
    return hshrink_op(x)


@constexpr
def _check_axis_in_range(axis, ndim):
    """Checks axes are with the bounds of ndim"""
    if not isinstance(axis, int):
        raise TypeError(f'The dims must be integers, but got {type(axis)}')
    if not -ndim <= axis < ndim:
        raise ValueError(f"The 'axis' must be in the range of [-{ndim}, {ndim}), but got {axis}.")
    return axis % ndim


@constexpr
def _check_axis_valid(axes, ndim):
    """
    Checks axes are valid given ndim, and returns axes that can be passed
    to the built-in operator (non-negative, int or tuple)
    """
    if axes is None:
        raise ValueError(f"The parameter dims can not be None.")
    if isinstance(axes, (tuple, list)):
        axes = tuple(map(lambda x: _check_axis_in_range(x, ndim), axes))
        if any(axes.count(el) > 1 for el in axes):
            raise ValueError(f"The element of parameter 'dims' can not be duplicate, but got {axes}.")
        return axes
    raise ValueError(f"The parameter dims must be tuple of ints, but got {type(axes)}")


@constexpr
def _get_flip_start(ndim, shape, axes):
    """Calculate the start index of flip"""
    return tuple([shape[i] - 1 if i in axes else 0 for i in range(ndim)])


@constexpr
def _get_flip_end(ndim, shape, axes):
    """Calculate the end index of flip"""
    return tuple([-shape[i] - 1 if i in axes else shape[i] + 1 for i in range(ndim)])


@constexpr
def _get_flip_strides(ndim, axes):
    """Calculate the strides of flip"""
    return tuple([-1 if i in axes else 1 for i in range(ndim)])


@constexpr
def _is_shape_empty(shp):
    """Check whether shape contains zero"""
    if isinstance(shp, int):
        return shp == 0
    return ops.shape_mul(shp) == 0


def _check_input_tensor(arg_name, *tensors):
    """Check whether the input is tensor"""
    for tensor in tensors:
        if not isinstance(tensor, Tensor):
            raise TypeError(f"For '{arg_name}', the input must be Tensor, but got {ops.typeof(tensor)}")
    return True


def flip(x, dims):
    """
    Reverses the order of elements in a tensor along the given axis.

    The shape of the tensor is preserved, but the elements are reordered.

    Args:
        x (Tensor): Input tensor.
        dims (Union[list[int], tuple[int]]): Axis or axes along which to flip over.
            Flipping is performed on all of the axes specified in the tuple,
            If `dims` is a tuple of integers contains negative, it counts from the last to the first axis.

    Returns:
        Tensor, with the entries of `dims` reversed.

    Raises:
        TypeError: If the input is not a tensor.
        ValueError: If `dims` is None.
        ValueError: If `dims` is not a tuple of ints.

    Supported Platforms:
        ``GPU`` ``CPU``

    Examples:
        >>> import mindspore as ms
        >>> import mindspore.ops as ops
        >>> import numpy as np
        >>> x = ms.Tensor(np.arange(8).reshape((2, 2, 2)))
        >>> output = ops.flip(x, (0, 2))
        >>> print(output)
        [[[5. 4.]
        [7. 6.]]
        [[1. 0.]
        [3. 2.]]]
    """
    _check_input_tensor("flip", x)
    ndim = ops.rank(x)
    shape = ops.shape(x)
    dims = _check_axis_valid(dims, ndim)
    if _is_shape_empty(shape):
        return x
    start = _get_flip_start(ndim, shape, dims)
    end = _get_flip_end(ndim, shape, dims)
    strides = _get_flip_strides(ndim, dims)
    res = ops.strided_slice(x, start, end, strides)
    return res


def flipud(x):
    """
    Flips the entries in each column in the up/down direction.
    Rows are preserved, but appear in a different order than before.

    Args:
        x (Tensor): Input array.

    Returns:
        Tensor.

    Raises:
        TypeError: If the input is not a tensor.

    Supported Platforms:
        ``GPU`` ``CPU``

    Examples:
        >>> import mindspore as ms
        >>> import mindspore.ops as ops
        >>> import numpy as np
        >>> x = ms.Tensor(np.arange(8).reshape((2, 2, 2)))
        >>> output = ops.flipud(x)
        >>> print(output)
        [[[4. 5.]
        [6. 7.]]
        [[0. 1.]
        [2. 3.]]]
    """
    return flip(x, (0,))


def fliplr(x):
    """
    Flips the entries in each row in the left/right direction.
    Columns are preserved, but appear in a different order than before.

    Args:
        x (Tensor): Input tensor.

    Returns:
        Tensor.

    Raises:
        TypeError: If the input is not a tensor.

    Supported Platforms:
        ``GPU`` ``CPU``

    Examples:
        >>> import mindspore as ms
        >>> import mindspore.ops as ops
        >>> import numpy as np
        >>> x = ms.Tensor(np.arange(8).reshape((2, 2, 2)))
        >>> output = ops.fliplr(x)
        >>> print(output)
        [[[2. 3.]
        [0. 1.]]
        [[6. 7.]
        [4. 5.]]]
    """
    return flip(x, (1,))


def is_floating_point(x):
    """
    Judge whether the data type of `x` is a floating point data type i.e., one of mindspore.flot64, mindspore.float32,
    mindspore.float16.

    Args:
        x (Tensor): The input Tensor.

    Returns:
        Bool. If the dtype of `x` is a floating point data type, return True. Otherwise, return False.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> import mindspore as ms
        >>> import mindspore.ops as ops
        >>> from mindspore import Tensor
        >>> x = ms.Tensor([1, 2, 3], ms.float32)
        >>> y = ms.Tensor([1, 2, 3], ms.int64)
        >>> output = ops.is_floating_point(x)
        >>> output2 = ops.is_floating_point(y)
        >>> print(output)
        True
        >>> print(output2)
        False
    """
    return x.dtype in [mstype.float32, mstype.float16, mstype.float64]


def hardswish(x):
    r"""
    Applies hswish-type activation element-wise. The input is a Tensor with any valid shape.

    Hard swish is defined as:

    .. math::

        \text{hswish}(x_{i}) = x_{i} * \frac{ReLU6(x_{i} + 3)}{6},

    where :math:`x_i` is an element of the input Tensor.

    Args:
        x (Tensor): The input to compute the Hard Swish with data type of float16 or float32.

    Returns:
        Tensor, has the same data type and shape as the input.

    Raises:
        TypeError: If `x` is not a Tensor.
        TypeError: If dtype of `x` is neither float16 nor float32.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> x = Tensor(np.array([-1, -2, 0, 2, 1]), mindspore.float16)
        >>> output = ops.hardswish(x)
        >>> print(output)
        [-0.3333  -0.3333  0  1.666  0.6665]
    """
    return hardswish_(x)


@constexpr
def _check_interpolate_inputs(input_dims, roi, scales, sizes, coordinate_transformation_mode, mode,
                              prim_name):
    """Check input"""
    msg_prefix = f"For '{prim_name}', the"
    validator.check_value_type("coordinate_transformation_mode", coordinate_transformation_mode, [str], prim_name)
    support_coordinate_mode_list = ["align_corners", "half_pixel", "asymmetric"]
    if coordinate_transformation_mode not in support_coordinate_mode_list:
        raise TypeError(f"{msg_prefix} coordinate_transformation_mode must be in {support_coordinate_mode_list},"
                        " but got {coordinate_transformation_mode}")
    validator.check_value_type("mode", mode, [str], prim_name)
    if mode == "linear":
        validator.check_int(input_dims, 3, Rel.EQ, "input dims", prim_name)
    elif mode == "bilinear":
        validator.check_int(input_dims, 4, Rel.EQ, "input dims", prim_name)
    else:
        raise ValueError(f"{msg_prefix} mode must be 'linear' or 'bilinear', but got {mode}")

    if sizes is None and scales is None:
        raise ValueError(f"{msg_prefix} 'sizes' and 'scale' both none.")
    if sizes is not None and scales is not None:
        raise ValueError(f"{msg_prefix} 'sizes' and 'scale' both not none.")
    if sizes is not None:
        if not isinstance(sizes, tuple):
            raise TypeError(
                f"{msg_prefix} 'sizes' must be tuple or None, but got {type(sizes).__name__}.")
        for item in sizes:
            validator.check_positive_int(item, 'sizes item', prim_name)
            validator.check_value_type("sizes item", item, int, prim_name)
        validator.check_int(len(sizes), input_dims - 2, Rel.EQ, "sizes", prim_name)
        return
    if not isinstance(scales, tuple):
        raise TypeError(
            f"{msg_prefix} 'scales' must be tuple or None, but got {type(scales).__name__}.")
    for item in scales:
        validator.check_positive_float(item, 'scales item', prim_name)
        validator.check_value_type("scales item", item, float, prim_name)
    scales_dims = len(scales)
    validator.check_int(scales_dims, input_dims, Rel.EQ, "scales dims", prim_name)
    validator.check_float(scales[0], 1.0, Rel.EQ, "scales[0]", prim_name)
    validator.check_float(scales[1], 1.0, Rel.EQ, "scales[1]", prim_name)


def _interpolate_output_shape(shape, scales, sizes, mode):
    """calculate output shape"""
    if sizes is not None:
        if mode == "bilinear":
            return sizes
        return Tensor(sizes)
    ret = ()
    for i in range(2, len(shape)):
        ret = ret + (int(scales[i] * shape[i]),)
    if mode == "bilinear":
        return ret
    return Tensor(ret)


def interpolate(x, roi=None, scales=None, sizes=None, coordinate_transformation_mode="align_corners", mode="linear"):
    r"""
    Using the interpolate method specified by `mode` resize the input tensor `x`.

    .. warning::
        - This is an experimental prototype that is subject to change.
        - The `roi` is reserved interface for 'crop_and_resize' coordinate transformation mode,
          which is not support now.
        - The Ascend platforms is currently not supported when `mode` is "linear".
        - The 'half_pixel' coordinate_transformation_mode is currently not supported on CPU device
          when mode is "bilinear".

    Args:
        x (Tensor): a tensor which to resize. `x` is a 3-D tensor when `mode` is "linear". `x` is a 4-D tensor when
            `mode` is "bilinear".
        roi (tuple[float], optional): a tuple of float. Only takes effect when attr coordinate_transformation_mode is
            'crop_and_resize'.
        scales (tuple[float], optional): a tuple of float. Describe the scale along each dimension.
            Its length is the same as that of shape of `x`. The numbers in `scales` must all be positive. Only one of
            `scales` and `sizes` can be specified.
        sizes (tuple[int], optional): a tuple of int, describes the shape of the output tensor. The numbers in `sizes`
            must all be positive. Only one of `scales` and `sizes` can be specified.  If `sizes` is specified, then set
            `scales` to 'None' in this operator's input list. It is 1 int elements :math:`(new\_width,)` when `mode`
            is "linear". It is 2 int elements :math:`(new\_height, new\_width)` when `mode` is "bilinear".
        coordinate_transformation_mode (str): Default is 'align_corners'. Describes how to transform the coordinate
            in the resized tensor to the coordinate in the original tensor. Other optional: 'half_pixel', 'asymmetric'.
            For example, we want to resize the original tensor along axis x. Let's denote `new_i` as the i-th coordinate
            of the resized tensor along axis x, `old_i` as the coordinate of the original tensor along axis x,
            `new_length` as the length of the resized tensor along axis x, `old_length` as the length of the original
            tensor along axis x. We compute the `old_i` via the following formula:

            .. code-block::

                old_i = new_length != 1 ? new_i * (old_length - 1) / (new_length - 1) : 0  # if set to 'align_corners'

                old_i = new_length > 1 ? (new_x + 0.5) * old_length / new_length - 0.5 : 0  # if set to 'half_pixel'

                old_i = new_length != 0 ? new_i * old_length / new_length : 0  # if set to 'asymmetric'

        mode (str): The method used to interpolate: 'linear' | 'bilinear'. Default is 'linear'.

    Returns:
        Resized tensor, with the same data type as input `x`.

    Raises:
        TypeError: If `x` is not a Tensor.
        TypeError: If the data type of `x` is not supported.
        TypeError: If `scales` is not a float tuple.
        ValueError: If not all numbers in `scales` are positive.
        TypeError: If `sizes` is not an int tuple.
        ValueError: If not all numbers in `sizes` are positive.
        TypeError: If `coordinate_transformation_mode` is not a string.
        ValueError: If `coordinate_transformation_mode` is not in the support list.
        TypeError: If `mode` is not a string.
        ValueError: If `mode` is not in the support list.

    Supported Platforms:
        ``Ascend`` ``CPU`` ``GPU``

    Examples:
        >>> # case 1: linear mode
        >>> x = Tensor([[[1, 2, 3], [4, 5, 6]]], mindspore.float32)
        >>> output = ops.interpolate(x, None, None, (6,), "align_corners")
        >>> print(output)
        [[[1. 1.4 1.8 2.2 2.6 3.]
          [4. 4.4 4.8 5.2 5.6 6.]]]
        >>> # case 2: bilinear mode
        >>> x = Tensor([[[[1, 2, 3, 4, 5], [1, 2, 3, 4, 5]]]], mindspore.float32)
        >>> output = ops.interpolate(x, None, None, (5, 5), "asymmetric", "bilinear")
        >>> print(output)
        [[[[1. 2. 3. 4. 5.]
           [1. 2. 3. 4. 5.]
           [1. 2. 3. 4. 5.]
           [1. 2. 3. 4. 5.]
           [1. 2. 3. 4. 5.]]]]
    """
    if not isinstance(x, (Tensor, Tensor_)):
        raise TypeError("For interpolate, the input x must be tensor")
    input_shape = x.shape
    input_dims = len(input_shape)
    _check_interpolate_inputs(input_dims, roi, scales, sizes, coordinate_transformation_mode, mode,
                              "interpolate")
    output_size = _interpolate_output_shape(input_shape, scales, sizes, mode)

    if mode == "linear":
        resize_linear_inner = _get_cache_prim(IMG.ResizeLinear1D)(
            coordinate_transformation_mode=coordinate_transformation_mode)
        return resize_linear_inner(x, output_size)
    if mode == "bilinear":
        align_corners = False
        half_pixel_centers = False
        if coordinate_transformation_mode == "align_corners":
            align_corners = True
        elif coordinate_transformation_mode == "half_pixel":
            half_pixel_centers = True
        resize_bilinear_inner = _get_cache_prim(IMG.ResizeBilinearV2)(align_corners, half_pixel_centers)
        return resize_bilinear_inner(x, output_size)

    raise TypeError(
        "Input Error: For interpolate,  {} mode is not support now".format(mode))


def softsign(x):
    r"""
    Softsign activation function.

    The function is shown as follows:

    .. math::
        \text{SoftSign}(x) = \frac{x}{1 + |x|}

    Args:
        x (Tensor): Tensor of shape :math:`(N, *)`, where :math:`*` means, any number of
            additional dimensions, with float16 or float32 data type.

    Returns:
        Tensor, with the same type and shape as the `x`.

    Raises:
        TypeError: If `x` is not a Tensor.
        TypeError: If dtype of `x` is neither float16 nor float32.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> x = Tensor(np.array([0, -1, 2, 30, -30]), mindspore.float32)
        >>> output = ops.softsign(x)
        >>> print(output)
        [ 0.        -0.5         0.6666667  0.9677419 -0.9677419]
    """
    return softsign_(x)


def softmax(x, axis=-1):
    r"""
    Applies the Softmax operation to the input tensor on the specified axis.
    Suppose a slice in the given axis :math:`x`, then for each element :math:`x_i`,
    the Softmax function is shown as follows:

    .. math::
        \text{output}(x_i) = \frac{exp(x_i)}{\sum_{j = 0}^{N-1}\exp(x_j)},

    where :math:`N` is the length of the tensor.

    Args:
        axis (Union[int, tuple[int]], optional): The axis to perform the Softmax operation. Default: -1.
        x (Tensor): Tensor of shape :math:`(N, *)`, where :math:`*` means, any number of
          additional dimensions, with float16 or float32 data type.

    Returns:
        Tensor, with the same type and shape as the logits.

    Raises:
        TypeError: If `axis` is not an int or a tuple.
        TypeError: If dtype of `x` is neither float16 nor float32.
        ValueError: If `axis` is a tuple whose length is less than 1.
        ValueError: If `axis` is a tuple whose elements are not all in range [-len(logits.shape), len(logits.shape))

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> x = Tensor(np.array([1, 2, 3, 4, 5]), mindspore.float32)
        >>> output = ops.softmax(x)
        >>> print(output)
        [0.01165623 0.03168492 0.08612854 0.23412167 0.6364086 ]
    """

    if not isinstance(axis, int):
        type_axis = type(axis).__name__
        raise TypeError(f" the type of 'axis' must be 'int', but got '{axis}' with type '{type_axis}'.")
    softmax_ = _get_cache_prim(P.Softmax)(axis=axis)
    return softmax_(x)


def soft_shrink(x, lambd=0.5):
    r"""
    Applies the SoftShrink function element-wise.

    .. math::
        \text{SoftShrink}(x) =
        \begin{cases}
        x - \lambda, & \text{ if } x > \lambda \\
        x + \lambda, & \text{ if } x < -\lambda \\
        0, & \text{ otherwise }
        \end{cases}

    Args:
        x (Tensor): The input of soft shrink with data type of float16 or float32.
        lambd(float): The :math:`\lambda` must be no less than zero. Default: 0.5.

    Returns:
        Tensor, has the same shape and data type as `x`.

    Raises:
        TypeError: If lambd is not a float.
        TypeError: If input_x is not a Tensor.
        TypeError: If dtype of input_x is neither float16 nor float32.
        ValueError: If lambd is less than 0.

    Supported Platforms:
        ``Ascend`` ``CPU`` ``GPU``

    Examples:
        >>> from mindspore import Tensor
        >>> from mindspore import ops
        >>> import numpy as np
        >>> x = Tensor(np.array([[ 0.5297,  0.7871,  1.1754], [ 0.7836,  0.6218, -1.1542]]), mindspore.float32)
        >>> output = ops.soft_shrink(x)
        >>> print(output)
        [[ 0.02979  0.287    0.676  ]
         [ 0.2837   0.1216  -0.6543 ]]
    """
    soft_shrink_op = _get_cache_prim(P.SoftShrink)(lambd)
    return soft_shrink_op(x)


def selu(input_x):
    r"""
    Activation function SeLU (Scaled exponential Linear Unit).

    The activation function is defined as:

    .. math::
        E_{i} =
        scale *
        \begin{cases}
        x_{i}, &\text{if } x_{i} \geq 0; \cr
        \text{alpha} * (\exp(x_i) - 1), &\text{otherwise.}
        \end{cases}

    where :math:`alpha` and :math:`scale` are pre-defined constants(:math:`alpha=1.67326324`
    and :math:`scale=1.05070098`).

    See more details in `Self-Normalizing Neural Networks <https://arxiv.org/abs/1706.02515>`_.

    Args:
        input_x (Tensor): Tensor of any dimension, the data type is float16 or float32.

    Returns:
        Tensor, with the same type and shape as the `input_x`.

    Raises:
        TypeError: If dtype of `input_x` is neither float16 nor float32.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> input_x = Tensor(np.array([[-1.0, 4.0, -8.0], [2.0, -5.0, 9.0]]), mindspore.float32)
        >>> output = ops.selu(input_x)
        >>> print(output)
        [[-1.1113307 4.202804 -1.7575096]
        [ 2.101402 -1.7462534 9.456309 ]]
    """
    return selu_(input_x)


def sigmoid(input_x):
    r"""
    Computes Sigmoid of input element-wise. The Sigmoid function is defined as:

    .. math::

        \text{sigmoid}(x_i) = \frac{1}{1 + \exp(-x_i)}

    where :math:`x_i` is an element of the input_x.

    Args:
        input_x (Tensor): Tensor of any dimension, the data type is float16, float32, float64, complex64 or complex128.

    Returns:
        Tensor, with the same type and shape as the input_x.

    Raises:
        TypeError: If dtype of `input_x` is not float16, float32, float64, complex64 or complex128.
        TypeError: If `input_x` is not a Tensor.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> input_x = Tensor(np.array([1, 2, 3, 4, 5]), mindspore.float32)
        >>> output = ops.sigmoid(input_x)
        >>> print(output)
        [0.7310586  0.880797   0.95257413 0.98201376 0.9933072 ]
    """
    return sigmoid_(input_x)


def deformable_conv2d(x, weight, offsets, kernel_size, strides, padding, bias=None, dilations=(1, 1, 1, 1), groups=1,
                      deformable_groups=1, modulated=True):
    r"""
    Given 4D tensor inputs `x`, `weight` and `offsets`, compute a 2D deformable convolution. The deformable convolution
    operation can be expressed as follow:

    Deformable Convolution v1:

    .. math::
        y(p)=\sum_{k=1}^{K}w_{k}\cdot x(p+p_{k}+\Delta{p_{k}})

    Deformable Convolution v2:

    .. math::
        y(p)=\sum_{k=1}^{K}w_{k}\cdot x(p+p_{k}+\Delta{p_{k}})\cdot \Delta{m_{k}}

    Where :math:`\Delta{p_{k}}` and :math:`\Delta{m_{k}}` are the learnable offset and modulation scalar for the k-th
    location. For details, please refer to `Deformable ConvNets v2: More Deformable, Better Results
    <https://arxiv.org/abs/1811.11168>`_ and `Deformable Convolutional Networks <https://arxiv.org/abs/1703.06211>`_.

    Args:
        x (Tensor): A 4D tensor of input image. With the format "NCHW",
            the shape is :math:`(N, C_{in}, H_{in}, W_{in})`. Dtype: float16 or float32.
        weight (Tensor): A 4D tensor of learnable filters. Must have the same type as `x`.
            The shape is :math:`(C_{out}, C_{in} / groups, H_{f}, W_{f})`.
        offsets (Tensor): A 4D tensor of x-y coordinates offset and mask. With the format "NCHW",
            the shape is :math:`(batch, 3 * deformable\_groups * H_{f} * W_{f}, H_{out}, W_{out})`. Note the C dimension
            is stored in the order of (offset_x, offset_y, mask). Must have the same type as `x`.
        kernel_size (tuple[int]): A tuple of 2 integers. The size of kernel.
        strides (tuple[int]): A tuple of 4 integers. The stride of the sliding window for each dimension of
            input. The dimension order is interpreted according to the data format of `x`. The N and C dimensions must
            be set to 1.
        padding (tuple[int]): A tuple of 4 integers. The number of pixels to add to each (top, bottom, left,
            right) side of the input.
        bias (Tensor, optional): An 1D tensor of additive biases to the filter outputs.
            The shape is :math:`(C_{out})`. Defaults to None.
        dilations (tuple[int], optional): A tuple of 4 integers. The dilation factor for each dimension of input. The
            dimension order is interpreted according to the data format of `x`. The N and C dimensions must be set
            to 1. Defaults to (1, 1, 1, 1).
        groups (int, optional): An integer of type int32. The number of blocked connections from input channels
            to output channels. In_channels and out_channels must both be divisible by `groups`. Defaults to 1.
        deformable_groups (int, optional): An integer of type int32. The number of deformable group partitions.
            In_channels must be divisible by `deformable_groups`. Defaults to 1.
        modulated (bool, optional): Specifies version of DeformableConv2D, True means v2, False means v1, currently
            only supports v2. Defaults to True.

    Returns:
        Tensor, A 4D Tensor of output feature map. With the same type as `x`. With the format "NCHW",
        the shape is :math:`(N, C_{out}, H_{out}, W_{out})`.

        .. math::
            \begin{array}{ll} \\
                H_{out} = \left \lfloor{\frac{H_{in} + padding[0] + padding[1] - (H_{f} - 1) \times
                \text{dilations[2]} - 1 }{\text{stride[0]}} + 1} \right \rfloor \\
                W_{out} = \left \lfloor{\frac{W_{in} + padding[2] + padding[3] - (W_{f} - 1) \times
                \text{dilations[3]} - 1 }{\text{stride[1]}} + 1} \right \rfloor \\
            \end{array}

    Raises:
        TypeError: If `strides`, `padding`, `kernel_size` or `dilations` is not a tuple with integer elements.
        TypeError: If `modulated` is not a bool.
        ValueError: If the tuple size of `strides`, `padding`, `kernel_size` or `dilations` is not expected.
        ValueError: The N or C dimensions of 'strides' or `dilations` is not set to 1.
        ValueError: If `modulated` is not set to True.

    Note:
        - This is an experimental interface that is subject to change or deletion.
        - For Ascend platform, only AI-CORE kernel is implemented, which has the following limitations:

          - :math:`C_{in}` cannot be divisible by 8 is not supported, e.g. `x` is :math:`(N, 2, H_{in}, W_{in})`.
          - `deformable_groups` must equal to 1.
          - `offsets` value is float which does not contain a decimal part is not supported, e.g. `offsets` is assigned
            with "numpy.ones()".
          - `kernel_size` should meet the requirement::math:`3 * kernel\_size[0] * kernel\_size[1] > 8`.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> x = Tensor(np.ones((4, 3, 10, 10)), mstype.float32)
        >>> kh, kw = 3, 3
        >>> weight = Tensor(np.ones((5, 3, kh, kw)), mstype.float32)
        >>> offsets = Tensor(np.ones((4, 3 * kh * kw, 8, 8)), mstype.float32)
        >>> output = ops.deformable_conv2d(x, weight, offsets, (kh, kw), (1, 1, 1, 1), (0, 0, 0, 0))
        >>> print(output.shape)
        (4, 5, 8, 8)
    """
    deformable_offsets = _get_cache_prim(NN_OPS.DeformableOffsets)(strides, padding, kernel_size, dilations, "NCHW",
                                                                   deformable_groups,
                                                                   modulated)
    fm_offset = deformable_offsets(x, offsets)

    weight_shape = weight.shape
    out_channel = weight_shape[0]
    strides_conv = (kernel_size[0], kernel_size[1])
    conv = _get_cache_prim(P.Conv2D)(out_channel, kernel_size, 1, "valid", 0, strides_conv, 1, groups)
    bias_add_ = _get_cache_prim(P.BiasAdd)()

    output = conv(fm_offset, weight)
    if bias is not None:
        output = bias_add_(output, bias)
    return output


def pdist(x, p=2.0):
    r"""
    Computes the p-norm distance between each pair of row vectors in the input. If `x` is a 2D Tensor of
    shape :math:`(N, M)`, then `output` must be a 1D Tensor of shape :math:`(N * (N - 1) / 2,)`. If `x` is a
    Tensor of shape :math:`(*B, N, M)`, then `output` must be a Tensor of shape :math:`(*B, N * (N - 1) / 2)`.

    .. math::
        y[n] = \sqrt[p]{{\mid x_{i} - x_{j} \mid}^p}

    where :math:`x_{i}, x_{j}` are two different row vectors in the input.

    Args:
        x (Tensor): Input tensor of shape :math:`(*B, N, M)`. :math:`*B` is batch size, one-dim or multi-dim.
            dtype: float16, float32 or float64.
        p (float): p value for the p-norm distance to calculate between each vector pair. :math:`p∈[0,∞]`. Default: 2.0.

    Returns:
        Tensor, has the same dtype as `x`.

    Raises:
        TypeError: If `x` is not a Tensor.
        TypeError: If dtype of `x` is not float16, float32 or float64.
        TypeError: If `p` is not a float.
        ValueError: If `p` is a negative float.
        ValueError: If dimension of `x` is less than 2.

    Supported Platforms:
        ``CPU``

    Examples:
        >>> x = Tensor(np.array([[1.0, 1.0], [2.0, 2.0], [3.0, 3.0]]).astype(np.float32))
        >>> y = ops.pdist(x, p=2.0)
        >>> print(y)
        [1.4142135 2.828427 1.4142135]
    """
    pdist_ = _get_cache_prim(NN_OPS.Pdist)(p=p)
    return pdist_(x)


@constexpr
def _check_pad_inputs(padding):
    """check the input of pad"""
    if len(padding) % 2 != 0:
        raise ValueError(f"For 'pad', the size of padding must be divisible by 2, but got {len(padding)}")
    if not isinstance(padding, (tuple, list)):
        raise TypeError(f"For 'pad', the type of 'paddings' must be a tuple of int or list of int or a Tensor,"
                        f" but got {type(padding)}.")
    for pd in padding:
        if not isinstance(pd, int):
            raise TypeError(f"For 'pad', the paddings value must be tuple of int or list of int, but got {padding}")


def pad(input_x, padding, mode='constant', value=None):
    r"""
    Pads the input tensor according to the padding.

    Args:
        input_x (Tensor): Tensor of shape :math:`(N, *)`, where :math:`*` means, any number of additional dimensions.
        padding (Union[tuple[int], list[int], Tensor]): Filling position of pad.
            :math:`\left\lfloor\frac{\text{len(padding)}}{2}\right\rfloor` dimensions
            of `input_x` will be padded.

            Example: to pad only the last dimension of the input tensor, then
            :attr:`padding` has the form
            :math:`(\text{padding_left}, \text{padding_right})`;

            Example: to pad the last 2 dimensions of the input tensor, then use
            :math:`(\text{padding_left}, \text{padding_right}`,
            :math:`\text{padding_top}, \text{padding_bottom})`;

            Example: to pad the last 3 dimensions, use
            :math:`(\text{padding_left}, \text{padding_right}`,
            :math:`\text{padding_top}, \text{padding_bottom}`,
            :math:`\text{padding_front}, \text{padding_back})` and so on.

        mode (str, optional): Pad filling mode, "constant", "reflect" or "replicate". Default: "constant".

            For "constant" mode, please refer to :class:`mindspore.nn.ConstantPad1d` as an example to understand
            this filling pattern and extend the padding pattern to n dimensions.

            For "reflect" mode, please refer to :class:`mindspore.nn.ReflectionPad1d` as an example
            and extend the padding pattern to n dimensions.

            For "replicate" mode, please refer to :class:`mindspore.nn.ReplicationPad1d` as an example
            and extend the padding pattern to n dimensions.

        value (Union[int, float, None], optional): Valid only in "constant" mode.
            Set the padding value in "constant" mode. If the value is None, 0 is used as the default padding value.

    Returns:
        Tensor, the tensor after padding.

    Raises:
        TypeError: If `paddings` is not an int of tuple or int of list.
        TypeError: If `input_x` is not a Tensor.
        ValueError: If padding.size is not equal to 2 * len(input_x).
        ValueError: If mode is not "constant" and value not None.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> import mindspore as ms
        >>> import mindspore.ops as ops
        >>> import numpy as np
        >>> x = ms.Tensor(np.arange(1 * 2 * 2 * 2).reshape((1, 2, 2, 2)), dtype=ms.float64)
        >>> output = ops.pad(x, [1, 0, 0, 1], mode='constant', value=6.0)
        >>> print(x)
        [[[[6. 0. 1.]
           [6. 2. 3.]
           [6. 6. 6.]]
          [[6. 4. 5.]
           [6. 6. 7.]
           [6. 6. 6.]]]]
        >>> output1 = ops.pad(x, (1, 0, 0, 1), mode='reflect')
        >>> print(output1)
        [[[[1. 0. 1.]
           [3. 2. 3.]
           [1. 0. 1.]]
          [[5. 4. 5.]
           [7. 6. 7.]
           [5. 4. 5.]]]]
        >>> output2 = ops.pad(x, (1, 1, 2, 1), mode='replicate')
        [[[[0. 0. 1. 1.]
           [0. 0. 1. 1.]
           [0. 0. 1. 1.]
           [2. 2. 3. 3.]
           [2. 2. 3. 3.]]
          [[4. 4. 5. 5.]
           [4. 4. 5. 5.]
           [4. 4. 5. 5.]
           [6. 6. 7. 7.]
           [6. 6. 7. 7.]]]]
    """
    if not isinstance(input_x, Tensor):
        raise TypeError(f"For 'pad', the type of 'input_x' must be Tensor, but got {type(input_x)}.")
    if (isinstance(padding, (tuple, list)) and not padding) or (isinstance(padding, Tensor) and padding.shape == (0,)):
        return input_x
    if not isinstance(padding, Tensor):
        _check_pad_inputs(padding)
        padding = Tensor(padding)
    if mode == "constant":
        value = 0 if value is None else value
        if isinstance(value, (float, int)):
            value = scalar_to_tensor_(value, input_x.dtype)
    else:
        if value is not None:
            raise ValueError(f"For 'pad', the padding mode '{mode}' can not set value, but got value {value}.")
        if mode == "replicate":
            mode = "edge"
    out = PadV3(mode=mode, paddings_contiguous=True)(input_x, padding, value)
    return out


def relu(x):
    r"""
    Computes ReLU (Rectified Linear Unit activation function) of input tensors element-wise.

    It returns :math:`\max(x,\  0)` element-wise. Specially, the neurons with the negative output
    will be suppressed and the active neurons will stay the same.

    .. math::

        ReLU(x) = (x)^+ = max(0, x)

    Note:
        In general, this operator is more commonly used. The difference from `ReLuV2` is that the `ReLuV2` will
        output one more Mask.

    Args:
        x (Tensor): Tensor of shape :math:`(N, *)`, where :math:`*` means, any number of
          additional dimensions, data type is
          `number <https://www.mindspore.cn/docs/en/r2.0.0-alpha/api_python/mindspore.html#mindspore.dtype>`_.

    Returns:
        Tensor of shape :math:`(N, *)`, with the same dtype and shape as the `x`.

    Raises:
        TypeError: If dtype of `x` is not a number.
        TypeError: If `x` is not a Tensor.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> input_x = Tensor(np.array([[-1.0, 4.0, -8.0], [2.0, -5.0, 9.0]]), mindspore.float32)
        >>> output = ops.relu(input_x)
        >>> print(output)
        [[0. 4. 0.]
         [2. 0. 9.]]
    """
    relu_ = _get_cache_prim(NN_OPS.ReLU)()
    return relu_(x)


def relu6(x):
    r"""
    Computes ReLU (Rectified Linear Unit) upper bounded by 6 of input tensors element-wise.

    .. math::

        \text{ReLU6}(x) = \min(\max(0,x), 6)

    It returns :math:`\min(\max(0,x), 6)` element-wise.

    Args:
        x (Tensor): Tensor of shape :math:`(N, *)`, where :math:`*` means, any number of
          additional dimensions, with float16 or float32 data type.

    Returns:
        Tensor, with the same dtype and shape as the `x`.

    Raises:
        TypeError: If dtype of `x` is neither float16 nor float32.
        TypeError: If `x` is not a Tensor.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> input_x = Tensor(np.array([[-1.0, 4.0, -8.0], [2.0, -5.0, 9.0]]), mindspore.float32)
        >>> result = ops.relu6(input_x)
        >>> print(result)
        [[0. 4. 0.]
         [2. 0. 6.]]
    """
    relu6_ = _get_cache_prim(NN_OPS.ReLU6)()
    return relu6_(x)


def prelu(x, weight):
    r"""
    Parametric Rectified Linear Unit activation function.

    PReLU is described in the paper `Delving Deep into Rectifiers: Surpassing Human-Level Performance on
    ImageNet Classification <https://arxiv.org/abs/1502.01852>`_. Defined as follows:

    .. math::
        prelu(x_i)= \max(0, x_i) + \min(0, w * x_i),

    where :math:`x_i` is an element of a channel of the input, `w` is the weight of the channel.

    Note:
        Scalar or 1-D input x is not supported on Ascend.

    Args:
        x (Tensor): The input Tensor of the activation function. The data type is float16 or float32.
          The shape is :math:`(N, *)` where :math:`*` means, any number of additional dimensions.
        weight (Tensor):  Weight Tensor. The data type is float16 or float32.
          The weight can only be a vector, and the length is the same as the number of channels C of the `input_x`.
          On GPU devices, when the input is a scalar, the shape is (1,).

    Returns:
        Tensor, with the same shape and dtype as `x`.

    For detailed information, please refer to :class:`mindspore.nn.PReLU`.

    Raises:
        TypeError: If dtype of `x` or `weight` is neither float16 nor float32.
        TypeError: If the `x` or the `weight` is not a Tensor.
        ValueError: If the `x` is a 0-D or 1-D Tensor on Ascend.
        ValueError: If the `weight` is not a 1-D Tensor.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> x = Tensor(np.arange(-6, 6).reshape((2, 3, 2)), mindspore.float32)
        >>> weight = Tensor(np.array([0.1, 0.6, -0.3]), mindspore.float32)
        >>> output = ops.prelu(x, weight)
        >>> print(output)
        [[[-0.60 -0.50]
          [-2.40 -1.80]
          [ 0.60  0.30]]
         [[ 0.00  1.00]
          [ 2.00  3.00]
          [ 4.0   5.00]]]
    """
    prelu_ = _get_cache_prim(NN_OPS.PReLU)()
    return prelu_(x, weight)


def mirror_pad(input_x, paddings, mode):
    """
    Pads the input tensor according to the paddings and mode.

    Args:
        input_x (Tensor): Tensor of shape :math:`(N, *)`, where :math:`*` means, any number of
          additional dimensions.
        paddings (Tensor): Paddings requires constant tensor. The value of `paddings` is a
          matrix(list), and its shape is (N, 2). N is the rank of input data. All elements of paddings
          are int type. For the input in the `D` th dimension, paddings[D, 0] indicates how many sizes
          to be extended ahead of the input tensor in the `D` th dimension, and paddings[D, 1]
          indicates how many sizes to be extended behind the input tensor in the `D` th dimension. Both
          paddings[D, 0] and paddings[D, 1] must be no greater than input_x.dim_size(D)
          (or input_x.dim_size(D) - 1) if mode is SYMMETRIC (if REFLECT, respectively).
        mode (str): Specifies the padding mode. The optional values are "REFLECT" and "SYMMETRIC".
            Default: "REFLECT".

    Returns:
        Tensor, the tensor after padding.

        - If `mode` is "REFLECT", it uses a way of symmetrical copying through the axis of symmetry to fill in.
          If the `input_x` is [[1,2,3], [4,5,6], [7,8,9]] and `paddings` is [[1,1], [2,2]], then the
          `Outputs` is [[6,5,4,5,6,5,4], [3,2,1,2,3,2,1], [6,5,4,5,6,5,4], [9,8,7,8,9,8,7], [6,5,4,5,6,5,4]].
          For a more intuitive understanding, please see the example below.
        - If `mode` is "SYMMETRIC", the filling method is similar to the "REFLECT". It is also copied
          according to the symmetry axis, except that it includes the symmetry axis. If the `input_x`
          is [[1,2,3], [4,5,6], [7,8,9]] and `paddings` is [[1,1], [2,2]], then the `Outputs` is
          [[2,1,1,2,3,3,2], [2,1,1,2,3,3,2], [5,4,4,5,6,6,5], [8,7,7,8,9,9,8], [8,7,7,8,9,9,8]].
          For a more intuitive understanding, please see the example below.

    Raises:
        TypeError: If `input_x` or `paddings` is not a Tensor.
        TypeError: If `mode` is not a str.
        ValueError: If paddings.size is not equal to 2 * rank of input_x.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> input_x = Tensor([[1,2,3], [4,5,6], [7,8,9]])
        >>> mode = "REFLECT"
        >>> paddings = Tensor([[1, 1], [2, 2]])
        >>> output = ops.mirror_pad(input_x, paddings, mode)
        >>> print(output)
        [[6 5 4 5 6 5 4]
         [3 2 1 2 3 2 1]
         [6 5 4 5 6 5 4]
         [9 8 7 8 9 8 7]
         [6 5 4 5 6 5 4]]
    """

    _mirror_pad = _get_cache_prim(P.MirrorPad)(mode)
    return _mirror_pad(input_x, paddings)


def _innner_log_softmax(inputs, axis):
    """inner implementation of log_softmax, since the LogSoftmaxGrad op do not support inputs > 2d"""
    return inputs - logsumexp(inputs, axis, True)


def cross_entropy(inputs, target, weight=None, ignore_index=-100, reduction='mean', label_smoothing=0.0):
    r"""
    The cross entropy loss between input and target.

    The cross entropy support two kind of targets:

    - Class indices (int) in the range :math:`[0, C)` where :math:`C` is the number of classes,
      the loss with reduction=none can be described as:

      .. math::

          \ell(x, y) = L = \{l_1,\dots,l_N\}^\top, \quad
          l_n = - w_{y_n} \log \frac{\exp(x_{n,y_n})}{\sum_{c=1}^C \exp(x_{n,c})}
          \cdot \mathbb{1}\{y_n \not= \text{ignore_index}\}

      where :math:`x` is the inputs, :math:`t` is the target, :math:`w` is the weight,
      N is the batch size, :math:`c` belonging to [0, C-1] is class index, where :math:`C` is the number of classes.

      If reduction is not 'none' (default 'mean'), then

      .. math::

          \ell(x, y) = \begin{cases}
              \sum_{n=1}^N \frac{1}{\sum_{n=1}^N w_{y_n} \cdot \mathbb{1}\{y_n \not= \text{ignore_index}\}} l_n, &
              \text{if reduction} = \text{'mean',}\\
              \sum_{n=1}^N l_n,  &
              \text{if reduction} = \text{'sum'.}
              \end{cases}

    - Probabilities (float) for each class, useful when labels beyond a single class per minibatch item
      are required, the loss with reduction=none can be described as:

      .. math::

          \ell(x, y) = L = \{l_1,\dots,l_N\}^\top, \quad
          l_n = - \sum_{c=1}^C w_c \log \frac{\exp(x_{n,c})}{\sum_{i=1}^C \exp(x_{n,i})} y_{n,c}

      where :math:`x` is the inputs, :math:`t` is the target, :math:`w` is the weight,
      N is the batch size, :math:`c` belonging to [0, C-1] is class index, where :math:`C` is the number of classes.

      If reduction is not 'none' (default 'mean'), then

      .. math::

          \ell(x, y) = \begin{cases}
              \frac{\sum_{n=1}^N l_n}{N}, &
              \text{if reduction} = \text{'mean',}\\
              \sum_{n=1}^N l_n,  &
              \text{if reduction} = \text{'sum'.}
              \end{cases}

    Args:
        inputs (Tensor): :math:`(N, C)` where `C = number of classes` or :math:`(N, C, H, W)`
            in case of 2D Loss, or :math:`(N, C, d_1, d_2, ..., d_K)`.
            `inputs` is expected to be log-probabilities, data type must be float16 or float32.
        target (Tensor): :math:`(N)` or :math:`(N, d_1, d_2, ..., d_K)` for
            high-dimensional loss.
        weight (Tensor): A rescaling weight applied to the loss of each batch element.
            If not None, the shape is :math:`(C,)`,
            data type must be float16 or float32. Default: None.
        ignore_index (int): Specifies a target value that is ignored
            and does not contribute to the input gradient. Default: -100
        reduction (str):  Apply specific reduction method to the output: 'none', 'mean', or 'sum'.
            Default: 'mean'.
        label_smoothing (float): Label smoothing values, a regularization tool used to prevent the model
            from overfitting when calculating Loss. The value range is [0.0, 1.0]. Default value: 0.0.

    Returns:
        Tensor, the computed loss value.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> # Case 1: Indices labels
        >>> inputs = mindspore.Tensor(np.random.randn(3, 5), mindspore.float32)
        >>> target = mindspore.Tensor(np.array([1, 0, 4]), mindspore.int32)
        >>> output = ops.cross_entropy(inputs, target)
        >>> # Case 2: Probability labels
        >>> inputs = mindspore.Tensor(np.random.randn(3, 5), mindspore.float32)
        >>> target = mindspore.Tensor(np.random.randn(3, 5), mindspore.float32)
        >>> output = ops.cross_entropy(inputs, target)
    """
    class_dim = 0 if inputs.ndim == 1 else 1
    if inputs.size == target.size:
        return _cross_entropy(inputs, target, class_dim, weight, reduction, label_smoothing)
    return nll_loss(_innner_log_softmax(inputs, class_dim), target, weight, ignore_index, reduction, label_smoothing)


def _cross_entropy(inputs, target, target_dim, weight=None, reduction='mean', label_smoothing=0.0):
    """cross entropy inner function"""
    _ones_like = _get_cache_prim(P.OnesLike)()

    class_dim = 0 if inputs.ndim == 1 else 1
    n_classes = inputs.shape[class_dim]
    inputs = _innner_log_softmax(inputs, class_dim)
    if label_smoothing > 0.0:
        target = target * (1 - label_smoothing) + label_smoothing / n_classes

    if weight is None:
        weight = _ones_like(inputs)
    else:
        broadcast_shape = [1 for _ in range(inputs.ndim)]
        broadcast_shape[1] = weight.shape[0]
        weight = weight.reshape(broadcast_shape)

    if reduction == 'mean':
        return -(inputs * target * weight).sum() / (inputs.size / n_classes)
    if reduction == 'sum':
        return -(inputs * target * weight).sum()
    return -(inputs * target * weight).sum(class_dim)


def nll_loss(inputs, target, weight=None, ignore_index=-100, reduction='mean', label_smoothing=0.0):
    r"""
    Gets the negative log likelihood loss between inputs and target.

    The nll loss with reduction=none can be described as:

    .. math::

        \ell(x, t)=L=\left\{l_{1}, \ldots, l_{N}\right\}^{\top},
        \quad l_{n}=-w_{t_{n}} x_{n, t_{n}},
        \quad w_{c}=\text { weight }[c] \cdot \mathbb{1}
        \{c \not= \text{ignore_index}\},

    where :math:`x` is the inputs, :math:`t` is the target, :math:`w` is the weight,
    N is the batch size, :math:`c` belonging to [0, C-1] is class index, where :math:`C` is the number of classes.

    If reduction is not 'none' (default 'mean'), then

    .. math::

        \ell(x, t)=\left\{\begin{array}{ll}
        \sum_{n=1}^{N} \frac{1}{\sum_{n=1}^{N} w_{t n}} l_{n}, & \text { if reduction }=\text { 'mean', } \\
        \sum_{n=1}^{N} l_{n}, & \text { if reduction }=\text { 'sum' }
        \end{array}\right.

    Args:
        inputs (Tensor): :math:`(N, C)` where `C = number of classes` or :math:`(N, C, H, W)`
            in case of 2D Loss, or :math:`(N, C, d_1, d_2, ..., d_K)`.
            `inputs` is expected to be log-probabilities, data type must be float16 or float32.
        target (Tensor): :math:`(N)` or :math:`(N, d_1, d_2, ..., d_K)` for
            high-dimensional loss, data type must be int32.
        weight (Tensor): A rescaling weight applied to the loss of each batch element.
            If not None, the shape is :math:`(C,)`.
            The data type must be float16 or float32. Default: None.
        ignore_index (int): Specifies a target value that is ignored
            and does not contribute to the input gradient. Default: -100
        reduction (str):  Apply specific reduction method to the output: 'none', 'mean', or 'sum'.
            Default: 'mean'.
        label_smoothing (float): Label smoothing values, a regularization tool used to prevent the model
            from overfitting when calculating Loss. The value range is [0.0, 1.0]. Default value: 0.0.

    Returns:
        Tensor, the computed loss value.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:

        >>> inputs = mindspore.Tensor(np.random.randn(3, 5), mindspore.float32)
        >>> target = mindspore.Tensor(np.array([1, 0, 4]), mindspore.int32)
        >>> output = ops.nll_loss(inputs, target)

    """
    ndim = inputs.ndim
    if ndim == 2:
        ret = _nll_loss(inputs, target, -1, weight, ignore_index, reduction, label_smoothing)
    elif ndim == 4:
        ret = _nll_loss(inputs, target, 1, weight, ignore_index, reduction, label_smoothing)
    elif ndim == 1:
        ret = _nll_loss(inputs, target, 0, weight, ignore_index, reduction, label_smoothing)
    else:
        n = inputs.shape[0]
        c = inputs.shape[1]
        out_size = (n,) + inputs.shape[2:]
        inputs = inputs.view(n, c, 1, -1)
        target = target.view(n, 1, -1)
        if reduction != 'none':
            ret = _nll_loss(inputs, target, 1, weight, ignore_index, reduction, label_smoothing)
        else:
            ret = _nll_loss(inputs, target, 1, weight, ignore_index, label_smoothing=label_smoothing)
            ret = ret.view(out_size)
    return ret


def _nll_loss(inputs, target, target_dim=-1, weight=None, ignore_index=None, reduction='none', label_smoothing=0.0):
    """nll loss inner function"""
    _neg = _get_cache_prim(P.Neg)()
    _gather_d = _get_cache_prim(P.GatherD)()
    _gather = _get_cache_prim(P.Gather)()
    _ones_like = _get_cache_prim(P.OnesLike)()
    _equal = _get_cache_prim(P.Equal)()

    if target.ndim == inputs.ndim - 1:
        target = target.expand_dims(target_dim)
    if ignore_index is not None:
        non_pad_mask = _equal(target, ignore_index)
        target = target.masked_fill(non_pad_mask, 0)
    else:
        non_pad_mask = target
    loss = _neg(_gather_d(inputs, target_dim, target))
    smooth_loss = _neg(inputs.sum(axis=target_dim, keepdims=True))
    if weight is not None:
        loss_weights = _gather(weight, target, 0)
        loss = loss * loss_weights
    else:
        loss_weights = _ones_like(loss)
    if ignore_index is not None:
        loss = loss.masked_fill(non_pad_mask, 0.)
        loss_weights = loss_weights.masked_fill(non_pad_mask, 0.)
        smooth_loss = smooth_loss.masked_fill(non_pad_mask, 0.)

    loss = loss.squeeze(target_dim)
    smooth_loss = smooth_loss.squeeze(target_dim)

    if reduction == 'sum':
        loss = loss.sum()
        smooth_loss = smooth_loss.sum()
    if reduction == 'mean':
        loss = loss.sum() / loss_weights.sum()
        smooth_loss = smooth_loss.mean()

    eps_i = label_smoothing / inputs.shape[target_dim]
    loss = (1. - label_smoothing) * loss + eps_i * smooth_loss

    return loss


def smooth_l1_loss(logits, labels, beta=1.0, reduction='none'):
    r"""
    Computes smooth L1 loss, a robust L1 loss.

    SmoothL1Loss is a Loss similar to MSELoss but less sensitive to outliers as described in the
    `Fast R-CNN <https://arxiv.org/abs/1504.08083>`_ by Ross Girshick.

    Given two input :math:`x,\  y` of length :math:`N`, the unreduced SmoothL1Loss can be described
    as follows:

    .. math::
        L_{i} =
        \begin{cases}
        \frac{0.5 (x_i - y_i)^{2}}{\text{beta}}, & \text{if } |x_i - y_i| < \text{beta} \\
        |x_i - y_i| - 0.5 \text{beta}, & \text{otherwise. }
        \end{cases}

    If `reduction` is not `none`, then:

    .. math::
        L =
        \begin{cases}
            \operatorname{mean}(L_{i}), &  \text{if reduction} = \text{'mean';}\\
            \operatorname{sum}(L_{i}),  &  \text{if reduction} = \text{'sum'.}
        \end{cases}

    Here :math:`\text{beta}` controls the point where the loss function changes from quadratic to linear.
    Its default value is 1.0. :math:`N` is the batch size.

    Note:
        For Ascend platform, the float64 data type of `logits` is not support now.

    Args:
        logits (Tensor): Tensor of shape :math:`(N, *)` where :math:`*` means, any number of additional dimensions.
        labels (Tensor): Ground truth data, tensor of shape :math:`(N, *)`, same shape and dtype as the `logits`.
        beta (float): A parameter used to control the point where the function will change from
            quadratic to linear. Default: 1.0.
        reduction (str): Apply specific reduction method to the output: 'none', 'mean' or 'sum'. Default: 'none'.

    Returns:
        Tensor, if `reduction` is 'none', then output is a tensor with the same shape as `logits`.
        Otherwise the shape of output tensor is `(1,)`.

    Raises:
        TypeError: If `beta` is not a float.
        ValueError: If `reduction` is not one of 'none', 'mean', 'sum'.
        TypeError: If dtype of `logits` or `labels` is neither float16 nor float32.
        ValueError: If `beta` is less than or equal to 0.
        ValueError: If shape of `logits` is not the same as `labels`.
        TypeError: The float64 data type of `logits` is support on Ascend platform.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> logits = Tensor(np.array([1, 2, 3]), mindspore.float32)
        >>> labels = Tensor(np.array([1, 2, 2]), mindspore.float32)
        >>> output = ops.smooth_l1_loss(logits, labels)
        >>> print(output)
        [0.  0.  0.5]
    """
    _smooth_l1_loss = _get_cache_prim(P.SmoothL1Loss)(beta, reduction)
    return _smooth_l1_loss(logits, labels)


def intopk(x1, x2, k):
    r"""
    Determines whether the targets are in the top `k` predictions.

    Args:
        x1 (Tensor): A 2D Tensor defines the predictions of a batch of samples with float16 or float32
          data type.
        x2 (Tensor): A 1D Tensor defines the labels of a batch of samples with int32 data type. The size of `x2`
          must be equal to the first dimension of `x1`. The values of `x2` can not be negative and
          must be equal to or less than index of x1's second dimension.
        k (int): Specifies the number of top elements to be used for computing precision along the last dimension.

    Returns:
        Tensor has 1 dimension of type bool and the same shape with `x2`. For labeling sample `i` in `x2`,
        if the label in the first `k` predictions for sample `i` is in `x1`, then the value is True, otherwise False.

    Raises:
        TypeError: If `k` is not an int.
        TypeError: If `x1` or `x2` is not a Tensor.
        TypeError: If dtype of `x1` is neither float16 nor float32.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> x1 = Tensor(np.array([[1, 8, 5, 2, 7], [4, 9, 1, 3, 5]]), mindspore.float32)
        >>> x2 = Tensor(np.array([1, 3]), mindspore.int32)
        >>> output = ops.intopk(x1, x2, 3)
        >>> print(output)
        [ True  False]
    """
    _in_topk = _get_cache_prim(P.InTopK)(k)
    return _in_topk(x1, x2)


def log_softmax(logits, axis=-1):
    r"""
    Applies the Log Softmax function to the input tensor on the specified axis.
    Supposes a slice in the given axis, :math:`x` for each element :math:`x_i`,
    the Log Softmax function is shown as follows:

    .. math::
        \text{output}(x_i) = \log \left(\frac{\exp(x_i)} {\sum_{j = 0}^{N-1}\exp(x_j)}\right),

    where :math:`N` is the length of the Tensor.

    Args:
        logits (Tensor): Tensor of shape :math:`(N, *)`, where :math:`*` means, any number of
          additional dimensions, with float16 or float32 data type.
        axis (int): The axis to perform the Log softmax operation. Default: -1.

    Returns:
        Tensor, with the same type and shape as the logits.

    Raises:
        TypeError: If `axis` is not an int.
        TypeError: If dtype of `logits` is neither float16 nor float32.
        ValueError: If `axis` is not in range [-len(logits.shape), len(logits.shape)).

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> logits = Tensor(np.array([1, 2, 3, 4, 5]), mindspore.float32)
        >>> output = ops.log_softmax(logits)
        >>> print(output)
        [-4.4519143 -3.4519143 -2.4519143 -1.4519144 -0.4519144]
    """
    _log_softmax = _get_cache_prim(P.LogSoftmax)(axis)
    return _log_softmax(logits)


def lrn(x, depth_radius=5, bias=1.0, alpha=1.0, beta=0.5, norm_region="ACROSS_CHANNELS"):
    r"""
    Local Response Normalization.

    .. math::

        b_{c} = a_{c}\left(k + \frac{\alpha}{n}
        \sum_{c'=\max(0, c-n/2)}^{\min(N-1,c+n/2)}a_{c'}^2\right)^{-\beta}

    where the :math:`a_{c}` indicates the specific value of the pixel corresponding to c in feature map;
    where the :math:`n/2` indicates the `depth_radius`; where the :math:`k` indicates the `bias`;
    where the :math:`\alpha` indicates the `alpha`; where the :math:`\beta` indicates the `beta`.

    Args:
        depth_radius (int): Half-width of the 1-D normalization window with the shape of 0-D. Default: 5.
        bias (float): An offset (usually positive to avoid dividing by 0). Default: 1.0.
        alpha (float): A scale factor, usually positive. Default: 1.0.
        beta (float): An exponent. Default: 0.5.
        norm_region (str): Specifies normalization region. Options: "ACROSS_CHANNELS". Default: "ACROSS_CHANNELS".
        x (Tensor): A 4-D Tensor with float16 or float32 data type.

    Returns:
        Tensor, with the same shape and data type as `x`.

    Raises:
        TypeError: If `depth_radius` is not an int.
        TypeError: If `bias`, `alpha` or `beta` is not a float.
        TypeError: If `norm_region` is not a str.
        TypeError: If `x` is not a Tensor.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> input_x = Tensor(np.array([[[[0.1], [0.2]],
        ...                       [[0.3], [0.4]]]]), mindspore.float32)
        >>> output = ops.lrn(input_x)
        >>> print(output)
        [[[[0.09534626]
           [0.1825742 ]]
          [[0.2860388 ]
           [0.3651484 ]]]]
    """
    lrn_op = NN_OPS.LRN(depth_radius, bias, alpha, beta, norm_region)
    return lrn_op(x)


def mish(x):
    r"""
    Computes MISH(A Self Regularized Non-Monotonic Neural Activation Function) of input tensors element-wise.

    The function is shown as follows:

    .. math::

        \text{output} = x * \tanh(\log(1 + \exp(\text{x})))

    See more details in `A Self Regularized Non-Monotonic Neural Activation Function
    <https://arxiv.org/abs/1908.08681>`_.

    Args:
        x (Tensor): Tensor of shape :math:`(N, *)`, where :math:`*` means, any number of
            additional dimensions, with float16 or float32 data type.

    Returns:
        Tensor, with the same type and shape as the `x`.

    Raises:
        TypeError: If dtype of `x` is neither float16 nor float32.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> input_x = Tensor(np.array([[-1.0, 4.0, -8.0], [2.0, -5.0, 9.0]]), mindspore.float32)
        >>> output = ops.mish(input_x)
        >>> print(output)
        [[-3.0340147e-01  3.9974129e+00 -2.68311895e-03]
         [ 1.9439590e+00  -3.3576239e-02 8.99999990e+00]]
    """
    return mish_(x)


@constexpr
def _check_value_type(arg_name, arg_value, valid_types, prim_name=None):
    """Checks whether a value is instance of some types."""
    return validator.check_value_type(arg_name, arg_value, valid_types, prim_name)


@constexpr(check=False)
def _check_is_tensor(param_name, input_data, cls_name):
    """Internal function, used to check whether the input data is Tensor."""
    if input_data is not None and not isinstance(ops.typeof(input_data), mstype.tensor_type):
        raise TypeError(f"For '{cls_name}', the '{param_name}' must be '{mstype.tensor_type}', "
                        f"but got '{ops.typeof(input_data)}'")


def _get_axis(x):
    """Get a range of axis for input."""
    shape = ops.shape(x)
    length = ops.tuple_len(shape)
    perm = ops.make_range(0, length)
    return perm


def _get_loss(x, reduction, cls_name, weights=1.0):
    """Calculate the loss with reduction and weights."""
    if reduction not in ('mean', 'sum', 'none'):
        raise ValueError(f"For '{cls_name}', the 'reduction' must be in ['mean', 'sum', 'none'], "
                         f"but got {reduction}.")

    reduce_mean = P.ReduceMean()
    reduce_sum = P.ReduceSum()
    mul = P.Mul()
    cast = P.Cast()

    input_dtype = x.dtype
    x = cast(x, mstype.float32)
    weights = cast(weights, mstype.float32)
    x = mul(weights, x)
    if reduction == 'mean':
        x = reduce_mean(x, _get_axis(x))
    if reduction == 'sum':
        x = reduce_sum(x, _get_axis(x))
    x = cast(x, input_dtype)
    return x


def margin_ranking_loss(input1, input2, target, margin=0.0, reduction='mean'):
    """
    MarginRankingLoss creates a criterion that measures the loss.

    For details, please refer to :class:`mindspore.nn.MarginRankingLoss`.
    """
    margin = _check_value_type("margin", margin, [float], "margin_ranking_loss")
    _check_is_tensor('input1', input1, "margin_ranking_loss")
    _check_is_tensor('input2', input2, "margin_ranking_loss")
    _check_is_tensor('target', target, "margin_ranking_loss")
    maximum = P.Maximum()
    inner.same_type_shape_(input1, input2)
    inner.same_type_shape_(target, input1)
    x = maximum(0, -target * (input1 - input2) + margin)
    return _get_loss(x, reduction, "margin_ranking_loss")


def max_pool3d(x, kernel_size, stride=None, padding=0, dilation=1, ceil_mode=False, return_indices=False):
    r"""
    Performs a 3D max pooling on the input Tensor.

    Typically the input is a Tensor with shape :math:`(N_{in}, C_{in}, D_{in}, H_{in}, W_{in})`, outputs
    regional maximum in the :math:`(D_{in}, H_{in}, W_{in})`-dimension. Given `kernel_size`
    :math:`ks = (d_{ker}, h_{ker}, w_{ker})` and `stride` :math:`s = (s_0, s_1, s_2)`, the operation is as follows:

    .. math::
        \text{output}(N_i, C_j, d, h, w) =
        \max_{l=0, \ldots, d_{ker}-1} \max_{m=0, \ldots, h_{ker}-1} \max_{n=0, \ldots, w_{ker}-1}
        \text{input}(N_i, C_j, s_0 \times d + l, s_1 \times h + m, s_2 \times w + n)

    Args:
        x (Tensor): Tensor of shape :math:`(N_{in}, C_{in}, D_{in}, H_{in}, W_{in})` with data type of int8,
            int16, int32, int64, uint8, uint16, uint32, uint64, float16, float32 or float64.
        kernel_size (Union[int, tuple[int]]): The size of kernel used to take the maximum value and arg
            value, is an int number that represents depth, height and width of the kernel, or a tuple of
            three int numbers that represent depth, height and width respectively.
        stride (Union[int, tuple[int]]): The distance of kernel moving, an int number that represents
            the depth, height and width of movement are both stride, or a tuple of three int numbers that
            represent depth, height and width of movement respectively. Default: `kernel_size`.
        padding (Union[int, tuple[int]]): An int number that represents the depth, height and width of movement are both
            strides, or a tuple of three int numbers that represent depth, height and width of movement respectively.
            Default: 0.
        dilation (Union[int, tuple[int]]): Control the stride of elements in the kernel. Default: 1.
        ceil_mode (bool): Whether to use ceil instead of floor to calculate output shape. Default: False.
        return_indices (bool): Whether to output the indices of max value. Default: False.

    Returns:
        If `return_indices` is False, return a Tensor `output`, else return a tuple (`output`, `argmax`).

        - **output** (Tensor) - Maxpooling result, with shape :math:`(N_{out}, C_{out}, D_{out}, H_{out}, W_{out})`.
          It has the same data type as `x`.
        - **argmax** (Tensor) - Index corresponding to the maximum value. Data type is int64. It will be return
          only when `return_indices` is True.

    Raises:
        TypeError: If `x` is not a Tensor.
        ValueError: If length of shape of `x` is not equal to 5.
        TypeError: If `kernel_size` , `stride` , `padding` or `dilation` is not int or tuple.
        ValueError: If `kernel_size` or `stride` is less than 1.
        ValueError: If `padding` is less than 0.

    Supported Platforms:
        ``GPU``

    Examples:
        >>> x = Tensor(np.arange(2 * 1 * 2 * 2 * 2).reshape((2, 1, 2, 2, 2)), mindspore.float32)
        >>> output_tensor, argmax = ops.max_pool3d(x, kernel_size=2, stride=1, padding=1, return_indices=True)
        >>> print(output_tensor.shape)
        (2, 1, 3, 3, 3)
        >>> print(argmax.shape)
        (2, 1, 3, 3, 3)
    """
    strides = stride if (stride is not None) else kernel_size
    max_pool3d_with_argmax_ = _get_cache_prim(NN_OPS.MaxPool3DWithArgmax)(
        kernel_size, strides, padding, dilation, ceil_mode)
    out, indices = max_pool3d_with_argmax_(x)
    if return_indices:
        return out, indices
    return out


def grid_sample(input_x, grid, interpolation_mode='bilinear', padding_mode='zeros', align_corners=False):
    """
    Given an `input_x` and a flow-field `grid`, computes the `output` using `input_x` values and pixel locations from
    `grid`. Only spatial (4-D) and volumetric (5-D) `input_x` is supported.

    In the spatial (4-D) case, for `input_x` with shape :math:`(N, C, H_{in}, W_{in})` and `grid` with shape
    :math:`(N, H_{out}, W_{out}, 2)`, the `output` will have shape :math:`(N, C, H_{out}, W_{out})`.

    For each output location `output[n, :, h, w]`, the size-2 vector `grid[n, h, w]` specifies `input_x` pixel
    locations `x` and `y`, which are used to interpolate the output value `output[n, :, h, w]`. In the case of 5D
    inputs, `grid[n, d, h, w]`, specifies the `x`, `y`, `z` pixel locations for interpolating
    `output[n, :, d, h, w]`. And `interpolation_mode` argument specifies "nearest" or "bilinear" or "bicubic"
    (supported in 4D case only) interpolation method to sample the input pixels.

    `grid` specifies the sampling pixel locations normalized by the `input_x` spatial dimensions. Therefore, it should
    have most values in the range of :math:`[-1, 1]`.

    If `grid` has values outside the range of :math:`[-1, 1]`, the corresponding outputs are handled as defined by
    `padding_mode`. If `padding_mode` is set to be "zeros", use :math:`0` for out-of-bound grid locations. If
    `padding_mode` is set to be "border", use border values for out-of-bound grid locations. If `padding_mode` is set
    to be "reflection", use values at locations reflected by the border for out-of-bound grid locations. For location
    far away from the border, it will keep being reflected until becoming in bound.

    Args:
        input_x (Tensor): input with shape of :math:`(N, C, H_{in}, W_{in})` (4-D case) or :math:`(N, C, D_{in},
            H_{in}, W_{in})` (5-D case) and dtype of float32 or float64.
        grid (Tensor): flow-field with shape of :math:`(N, H_{out}, W_{out}, 2)` (4-D case) or :math:`(N, D_{out},
            H_{out}, W_{out}, 3)` (5-D case) and same dtype as `input_x`.
        interpolation_mode (str): An optional string specifying the interpolation method. The optional values are
            "bilinear", "nearest" or "bicubic". Default: "bilinear". Note: `bicubic` supports only 4-D input. When
            `interpolation_mode="bilinear"` and the input is 5-D, the interpolation mode used internally will actually
            be trilinear. However, when the input is 4-D, the interpolation mode will legistimately be bilinear.
        padding_mode (str): An optional string specifying the pad method. The optional values are "zeros", "border" or
            "reflection". Default: "zeros".
        align_corners (bool): An optional bool. If set to `True`, the extrema (-1 and 1) are considered as referring to
            the center points of the input’s corner pixels. If set to `False`, they are instead considered as referring
            to the corner points of the input’s corner pixels, making the sampling more resolution agnostic. Default:
            `False`.

    Returns:
        Tensor, dtype is the same as `input_x` and whose shape is :math:`(N, C, H_{out}, W_{out})` (4-D) and
        :math:`(N, C, D_{out}, H_{out}, W_{out})` (5-D).

    Raises:
        TypeError: If `input_x` or `grid` is not a Tensor.
        TypeError: If the dtypes of `input_x` and `grid` are inconsistent.
        TypeError: If the dtype of `input_x` or `grid` is not a valid type.
        TypeError: If `align_corners` is not a boolean value.
        ValueError: If the rank of `input_x` or `grid` is not equal to 4(4-D case) or 5(5-D case).
        ValueError: If the first dimension of `input_x` is not equal to that of `grid`.
        ValueError: If the last dimension of `grid` is not equal to 2(4-D case) or 3(5-D case).
        ValueError: If `interpolation_mode` is not "bilinear", "nearest", "bicubic" or a string value.
        ValueError: If `padding_mode` is not "zeros", "border", "reflection" or a string value.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> input_x = Tensor(np.arange(16).reshape((2, 2, 2, 2)).astype(np.float32))
        >>> grid = Tensor(np.arange(0.2, 1, 0.1).reshape((2, 2, 1, 2)).astype(np.float32))
        >>> output = ops.grid_sample(input_x, grid, interpolation_mode='bilinear', padding_mode='zeros',
        ...                          align_corners=True)
        >>> print(output)
        [[[[ 1.9      ]
           [ 2.1999998]]
          [[ 5.9      ]
           [ 6.2      ]]]
         [[[10.5      ]
           [10.8      ]]
          [[14.5      ]
           [14.8      ]]]]
    """
    if input_x.ndim == 4:
        _grid_sampler_2d = _get_cache_prim(NN_OPS.GridSampler2D)(interpolation_mode, padding_mode, align_corners)
        return _grid_sampler_2d(input_x, grid)
    _grid_sampler_3d = _get_cache_prim(NN_OPS.GridSampler3D)(interpolation_mode, padding_mode, align_corners)
    return _grid_sampler_3d(input_x, grid)


@constexpr
def _check_ctc_loss_inputs(blank, reduction, zero_infinity, prim_name):
    validator.check_value_type("blank", blank, [int], prim_name)
    validator.check_value_type('reduction', reduction, [str], prim_name)
    validator.check_string(reduction, ['none', 'sum', 'mean'], 'reduction', prim_name)
    validator.check_value_type("zero_infinity", zero_infinity, [bool], prim_name)


def ctc_loss(log_probs, targets, input_lengths, target_lengths, blank=0, reduction="mean", zero_infinity=False):
    """
    Calculates the CTC (Connectionist Temporal Classification) loss and the gradient.

    The CTC algorithm is proposed in `Connectionist Temporal Classification: Labeling Unsegmented Sequence Data with
    Recurrent Neural Networks <http://www.cs.toronto.edu/~graves/icml_2006.pdf>`_.

    Args:
        log_probs (Tensor): A tensor of shape (T, N, C), where T is input length, N is batch size and C is
            number of classes (including blank).
        targets (Tensor): A tensor of shape (N, S), where S is max target length, means the target sequences.
        input_lengths (Union(Tuple, Tensor)): A tuple or Tensor of shape(N). It means the lengths of the input.
        target_lengths (Union(Tuple, Tensor)): A tuple or Tensor of shape(N). It means the lengths of the target.
        blank (int): The blank label. Default: 0.
        reduction (string): Apply specific reduction method to the output: 'none', 'mean', or 'sum'. Default: 'mean'.
        zero_infinity (bool): Whether to set infinite loss and correlation gradient to zero. Default: False.

    Returns:
        neg_log_likelihood (Tensor), A loss value with shape (N), which is differentiable with respect to
        each input node.

        log_alpha (Tensor), The probability of possible trace of input to target with shape (N, T, 2 * S + 1).

    Raises:
        TypeError: If `zero_infinity` is not a bool, reduction is not string.
        TypeError: If the dtype of `log_probs` or `grad_out` is not float or double.
        TypeError: If the dtype of `targets`, `input_lengths` or `target_lengths` is not int32 or int64.
        ValueError: If the rank of `log_probs` is not 3.
        ValueError: If the rank of `targets` is not 2.
        ValueError: If the shape of `input_lengths` does not match {batch_size|N}.
        ValueError: If the shape of `target_lengths` does not match {batch_size|N}.
        TypeError: If the types of `targets`, `input_lengths`, `grad_out` or `target_lengths` are different.
        ValueError: If the value of `blank` is not in range [0, num_labels|C).
        RuntimeError: If any value of `input_lengths` is larger than (num_labels|C).
        RuntimeError: If any target_lengths[i] is not in range [0, input_length[i]].

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> log_probs = Tensor(np.array([[[0.3, 0.6, 0.6]],
        ...                              [[0.9, 0.4, 0.2]]]).astype(np.float32))
        >>> targets = Tensor(np.array([[0, 1]]), mstype.int32)
        >>> input_lengths = Tensor(np.array([2]), mstype.int32)
        >>> target_lengths = Tensor(np.array([1]), mstype.int32)
        >>> loss, log_alpha = ops.ctc_loss(log_probs, targets, input_lengths,
        ...                                target_lengths, 0, 'mean', True)
        >>> print(loss)
        -2.2986124
        >>> print(log_alpha)
        [[[0.3       0.3            -inf      -inf      -inf]
          [1.2       1.8931472 1.2            -inf      -inf]]]
    """
    _check_ctc_loss_inputs(blank, reduction, zero_infinity, 'ctc_loss')
    ctc_loss_op = NN_OPS.CTCLossV2(blank=blank, reduction="none", zero_infinity=zero_infinity)
    loss, log_alpha = ctc_loss_op(log_probs, targets, input_lengths, target_lengths)
    if reduction == 'sum':
        loss = loss.sum()
    if reduction == 'mean':
        input_type = loss.dtype
        target_length_t = target_lengths.clip(1., None)
        loss = loss.astype("float32")
        loss = loss / target_length_t
        loss = loss.mean()
        loss = loss.astype(input_type)
    return (loss, log_alpha)


@constexpr
def _check_gaussian_nll_loss(full, eps, reduction):
    validator.check_value_type('full', full, [bool], 'gaussian_nll_loss')
    validator.check_positive_float(eps, 'eps', 'gaussian_nll_loss')
    validator.check_string(reduction, ['none', 'mean', 'sum'], 'reduction', 'gaussian_nll_loss')


def gaussian_nll_loss(x, target, var, full=False, eps=1e-6, reduction='mean'):
    r"""
    Gaussian negative log likelihood loss.

    The targets are treated as samples from Gaussian distributions with expectations and variances predicted by the
    neural network. For a `target` tensor modelled as having Gaussian distribution with a tensor of expectations
    `x` and a tensor of positive variances `var` the loss is:

    .. math::
        \text{loss} = \frac{1}{2}\left(\log\left(\text{max}\left(\text{var},
        \ \text{eps}\right)\right) + \frac{\left(\text{x} - \text{target}\right)^2}
        {\text{max}\left(\text{var}, \ \text{eps}\right)}\right) + \text{const.}

    where `eps` is used for stability of :math:`log`. By default, the constant term of the loss function is omitted
    unless :math:`full=True`. If the shape of :math:`var` is not the same as `x` (due to a
    homoscedastic assumption), it must either have a final dimension of 1 or have one fewer dimension
    (with all other sizes being the same) for correct broadcasting.

    Args:
        x (Tensor): Tensor of shape :math:`(N, *)` or :math:`(*)` where :math:`*` means any number of
            additional dimensions.
        target (Tensor): Tensor of shape :math:`(N, *)` or :math:`(*)`, same shape as the x, or same shape
            as the x but with one dimension equal to 1 (to allow broadcasting).
        var (Tensor): Tensor of shape :math:`(N, *)` or :math:`(*)`, same shape as x, or same shape as the x
            but with one dimension equal to 1, or same shape as the x but with one fewer dimension
            (to allow for broadcasting).
        full (bool, optional): Include the constant term in the loss calculation. When :math:`full=True`,
            the constant term `const.` will be :math:`0.5 * log(2\pi)`. Default: False.
        eps (float, optional): Used to improve the stability of log function must be greater than 0. Default: 1e-6.
        reduction (str, optional): Apply specific reduction method to the output: 'none', 'mean', or 'sum'.
            Default: 'mean'.

    Returns:
        Tensor or Tensor scalar, the computed loss depending on `reduction`.

    Raises:
        TypeError: If `x` is not a Tensor.
        TypeError: If `target` is not a Tensor.
        TypeError: If `var` is not a Tensor.
        TypeError: If `full` is not a bool.
        TypeError: If `eps` is not a float.
        ValueError: If `eps` is not a float within [0, inf).
        ValueError: If `reduction` is not one of 'none', 'mean', 'sum'.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> import numpy as np
        >>> from mindspore import Tensor
        >>> import mindspore.ops as ops
        >>> import mindspore.common.dtype as mstype
        >>> arr1 = np.arange(8).reshape((4, 2))
        >>> arr2 = np.array([2, 3, 1, 4, 6, 4, 4, 9]).reshape((4, 2))
        >>> x = Tensor(arr1, mstype.float32)
        >>> var = Tensor(np.ones((4, 1)), mstype.float32)
        >>> target = Tensor(arr2, mstype.float32)
        >>> output = ops.gaussian_nll_loss(x, target, var)
        >>> print(output)
        1.4374993

    Reference:
        Nix, D. A. and Weigend, A. S., "Estimating the mean and variance of the
        target probability distribution", Proceedings of 1994 IEEE International
        Conference on Neural Networks (ICNN'94), Orlando, FL, USA, 1994, pp. 55-60
        vol.1, doi: 10.1109/ICNN.1994.374138.
    """
    if not isinstance(x, Tensor):
        raise TypeError(f"For 'gaussian_nll_loss', 'x' must be a tensor, but got {type(x)}.")
    if not isinstance(target, Tensor):
        raise TypeError(f"For 'gaussian_nll_loss', 'target' must be a tensor, but got {type(target)}.")
    if not isinstance(var, Tensor):
        raise TypeError(f"For 'gaussian_nll_loss', 'var' must be a tensor, but got {type(var)}.")
    _check_gaussian_nll_loss(full, eps, reduction)
    max_op = P.Maximum()
    log_op = P.Log()
    square_op = P.Square()
    maxima = max_op(var, eps)
    logarithm = log_op(maxima)
    squared_loss = square_op(x - target)
    c = 0 if not full else 0.5 * log(2 * pi)
    loss = 0.5 * (logarithm + squared_loss / maxima) + c
    if reduction == 'mean':
        loss = loss.mean()
    elif reduction == 'sum':
        loss = loss.sum()
    return loss


@constexpr
def _check_hinge_embedding_loss(shape, shape2, prim_name):
    if shape2 != shape:
        raise ValueError(f"For '{prim_name}' the input tensor and the labels must have the same shape.")


def hinge_embedding_loss(inputs, targets, margin=1.0, reduction='mean'):
    r"""
    Hinge Embedding Loss. Compute the output according to the input elements. Measures the loss given an input tensor x
    and a labels tensor y (containing 1 or -1).
    This is usually used for measuring the similarity between two inputs.

    The loss function for :math:`n`-th sample in the mini-batch is

    .. math::
        l_n = \begin{cases}
        x_n, & \text{if}\; y_n = 1,\\
        \max \{0, \Delta - x_n\}, & \text{if}\; y_n = -1,
        \end{cases}

    and the total loss functions is

    .. math::
        \ell(x, y) = \begin{cases}
        \operatorname{mean}(L), & \text{if reduction} = \text{'mean';}\\
        \operatorname{sum}(L),  & \text{if reduction} = \text{'sum'.}
        \end{cases}

    where :math:`L = \{l_1,\dots,l_N\}^\top`.

    Args:
        inputs (Tensor): Tensor of shape :math:`(*)` where :math:`*` means any number of dimensions.
        targets (Tensor): Same shape as the logits, contains -1 or 1.
        margin (float): Threshold defined by Hinge Embedding Loss :math:`margin`.
            Represented as :math:`\Delta` in the formula. Default: 1.0.
        reduction (str): Specify the computing method to be applied to the outputs: 'none', 'mean', or 'sum'.
            Default: 'mean'.

    Returns:
        Tensor or Tensor scalar, the computed loss depending on `reduction`.

    Raises:
        TypeError: If `inputs` is not a Tensor.
        TypeError: If `targets` is not a Tensor.
        TypeError: If `margin` is not a float.
        ValueError: If `targets` does not have the same shape as `inputs`.
        ValueError: If `reduction` is not one of 'none', 'mean', 'sum'.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> import numpy as np
        >>> import mindspore.common.dtype as mstype
        >>> import mindspore.ops as ops
        >>> from mindspore import Tensor
        >>> arr1 = np.array([0.9, -1.2, 2, 0.8, 3.9, 2, 1, 0, -1]).reshape((3, 3))
        >>> arr2 = np.array([1, 1, -1, 1, -1, 1, -1, 1, 1]).reshape((3, 3))
        >>> logits = Tensor(arr1, mstype.float32)
        >>> labels = Tensor(arr2, mstype.float32)
        >>> loss = ops.hinge_embedding_loss(logits, labels, margin=1.0, reduction='mean')
        >>> print(loss)
        0.16666666
    """
    _shape = inputs.shape
    _dtype = inputs.dtype
    _t_shape = targets.shape
    _check_hinge_embedding_loss(_shape, _t_shape, 'HingeEmbeddingLoss')
    min_val = Tensor(0, _dtype)
    pos_index = targets > 0
    neg_index = targets < 0
    pos = pos_index * inputs
    neg = neg_index * inputs
    margin_matrix = margin * neg_index
    neg = margin_matrix - neg
    neg = ops.clip_by_value(neg, min_val)
    loss = pos + neg
    if reduction == 'mean':
        loss = loss.mean()
    elif reduction == 'sum':
        loss = loss.sum()
    return loss


def ctc_greedy_decoder(inputs, sequence_length, merge_repeated=True):
    r"""
    Performs greedy decoding on the logits given in inputs.

    Args:
        inputs (Tensor): The input Tensor must be a 3-D tensor whose shape is
            :math:`(max\_time, batch\_size, num\_classes)`. `num_classes` must be `num_labels + 1` classes,
            `num_labels` indicates the number of actual labels. Blank labels are reserved.
            Default blank label is `num_classes - 1`. Data type must be float32 or float64.
        sequence_length (Tensor): A tensor containing sequence lengths with the shape of :math:`(batch\_size, )`.
            The type must be int32. Each value in the tensor must be equal to or less than `max_time`.
        merge_repeated (bool): If true, merge repeated classes in output. Default: True.

    Returns:
        decoded_indices (Tensor), A tensor with shape of :math:`(total\_decoded\_outputs, 2)`.
        Data type is int64.

        decoded_values (Tensor), A tensor with shape of :math:`(total\_decoded\_outputs, )`,
        it stores the decoded classes. Data type is int64.

        decoded_shape (Tensor), A tensor with shape of :math:`(batch\_size, max\_decoded\_length)`.
        Data type is int64.

        log_probability (Tensor), A tensor with shape of :math:`(batch\_size, 1)`,
        containing sequence log-probability, has the same type as `inputs`.

    Raises:
        TypeError: If `merge_repeated` is not a bool.
        ValueError: If length of shape of `inputs` is not equal to 3.
        ValueError: If length of shape of `sequence_length` is not equal to 1.
        ValueError: If value in the `sequence_length` is larger than `max_time`.

    Supported Platforms:
        ``Ascend`` ``CPU``

    Examples:
        >>> inputs = Tensor(np.array([[[0.6, 0.4, 0.2], [0.8, 0.6, 0.3]],
        ...                           [[0.0, 0.6, 0.0], [0.5, 0.4, 0.5]]]), mindspore.float32)
        >>> sequence_length = Tensor(np.array([2, 2]), mindspore.int32)
        >>> decoded_indices, decoded_values, decoded_shape, log_probability = ops.ctc_greedy_decoder(inputs,
        ...                                                                                          sequence_length)
        >>> print(decoded_indices)
        [[0 0]
         [0 1]
         [1 0]]
        >>> print(decoded_values)
        [0 1 0]
        >>> print(decoded_shape)
        [2 2]
        >>> print(log_probability)
        [[-1.2]
         [-1.3]]
    """
    _ctc_greedy_decoder = _get_cache_prim(NN_OPS.CTCGreedyDecoder)(merge_repeated)
    return _ctc_greedy_decoder(inputs, sequence_length)


def conv3d_transpose(inputs, weight, pad_mode='valid', padding=0, stride=1, dilation=1, group=1,
                     output_padding=0):
    r"""
    Computes a 3D transposed convolution, which is also known as a deconvolution
    (although it is not an actual deconvolution).

    Args:
        inputs (Tensor): The gradients with respect to the output of the convolution.
           The shape conforms to the default.
           data_format :math:`(N, C_{in}, D_{out}, H_{out}, W_{out})`. Currently dout data type only supports float16
           and float32.
        weight (Tensor): Set size of kernel is :math:`(K_d, K_h, K_w)`, then the shape is
           :math:`(C_{in}, C_{out}//group, K_d, K_h, K_w)`. Where :math:`group` is the Args parameter,
           :math:`//` is the symbol for integer division.
           Currently weight data type only supports float16 and float32.
        pad_mode (str): Specifies padding mode. The optional values are
            "same", "valid", "pad". Default: "valid".

            - same: Adopts the way of completion. The depth, height and width of the output will be equal to
              the input `x` divided by stride. The padding will be evenly calculated in head and tail, top and bottom,
              left and right directions possibility.
              Otherwise, the last extra padding will be calculated from the tail, bottom and the right side.
              If this mode is set, `pad` must be 0.

            - valid: Adopts the way of discarding. The possible largest depth, height and width of output
              will be returned without padding. Extra pixels will be discarded. If this mode is set, `pad`
              and `output_padding` must be 0.

            - pad: Implicit paddings on both sides of the input in depth, height and width. The number of `pad` will
              be padded to the input Tensor borders. `pad` must be greater than or equal to 0.

        padding (Union(int, tuple[int])): The padding value to be filled. Default: 0. If `padding` is an integer, the
            paddings of head, tail, top, bottom, left and right are the same, equal to pad. If `padding` is a tuple of
            six integers, the padding of head, tail, top, bottom, left and right equal to padding[0], padding[1],
            padding[2], padding[3], padding[4] and padding[5] correspondingly.
        stride (Union(int, tuple[int])): The distance of kernel moving, an int number that represents
            the depth, height and width of movement are both strides, or a tuple of three int numbers that
            represent depth, height and width of movement respectively. Default: 1.
        dilation (Union(int, tuple[int])): Specifies the space to use between kernel elements. Default: 1.
        group (int): Splits input into groups. Default: 1. Only 1 is currently supported.
        output_padding (Union(int, tuple[int])): Add extra size to each dimension of the output. Default: 0.


    Outputs:
        Tensor, the gradients with respect to the input of convolution 3D.
        Tensor of shape :math:`(N, C_{out}//group, D_{out}, H_{out}, W_{out})`,
        where :math:`group` is the Args parameter.

    Supported Platforms:
        ``Ascend`` ``GPU``

    Raises:
        TypeError: If `group` is not an int.
        TypeError: If `stride`, `padding` , `dilation` or `output_padding` is neither an int not a tuple.
        ValueError: If the rank of `inputs`, `weight` is not equal to 5.
        ValueError: If `stride` or `dilation` is less than 1.
        ValueError: if inputs[1], weight[1] and weight[2:5] i.e. `in_channel`, `out_channel` and `kernel_size` is less
                    than 1.
        ValueError: If `padding` is less than 0.
        ValueError: If `pad_mode` is not one of 'same', 'valid' nor 'pad'.
        ValueError: If `padding` is a tuple whose length is not equal to 6.
        ValueError: If `pad_mode` is not equal to 'padding' and `padding` is not equal to (0, 0, 0, 0, 0, 0).
        ValueError: If `data_format` is not 'NCDHW'.
        TypeError: If data type of dout and weight is not float16.

    Examples:
        >>> dout = Tensor(np.ones([32, 16, 10, 32, 32]), mindspore.float16)
        >>> weight = Tensor(np.ones([16, 3, 4, 6, 2]), mindspore.float16)
        >>> output = conv3d_transpose(dout, weight)
        >>> print(output.shape)
        (32, 3, 13, 37, 33)
    """
    if len(inputs.shape) != 5:
        raise_value_error("the rank of inputs tensor should be 5.")
    if len(weight.shape) != 5:
        raise_value_error("the rank of weight tensor should be 5.")
    in_channel = inputs.shape[1]
    out_channel = weight.shape[1]
    kernel_size = weight.shape[2:5]
    _conv_3d_transpose = _get_cache_prim(NN_OPS.Conv3DTranspose)(in_channel, out_channel, kernel_size, 1, pad_mode,
                                                                 padding, stride, dilation, group, output_padding)
    return _conv_3d_transpose(inputs, weight)


def conv2d(inputs, weight, pad_mode="valid", padding=0, stride=1, dilation=1, group=1):
    r"""
    Applies a 2D convolution over an input tensor.
    The input tensor is typically of shape :math:`(N, C_{in}, H_{in}, W_{in})`,
    where :math:`N` is batch size, :math:`C` is channel number, :math:`H` is height, :math:`W` is width, :math:`X_i` is
    the :math:`i^{th}` input value and :math:`b_i` indicates the deviation value of the :math:`i^{th}` input value.
    For each batch of shape :math:`(C_{in}, H_{in}, W_{in})`, the formula is defined as:

    .. math::

        out_j = \sum_{i=0}^{C_{in} - 1} ccor(W_{ij}, X_i) + b_j,

    where :math:`ccor` is the `cross-correlation <https://en.wikipedia.org/wiki/Cross-correlation>`_  operator,
    :math:`C_{in}` is the input channel number, :math:`j` ranges
    from :math:`0` to :math:`C_{out} - 1`, :math:`W_{ij}` corresponds to the :math:`i`-th channel of the :math:`j`-th
    filter and :math:`out_{j}` corresponds to the :math:`j`-th channel of the output. :math:`W_{ij}` is a slice
    of kernel and it has shape :math:`(\text{kernel_size[0]}, \text{kernel_size[1]})`, where :math:`\text{
    kernel_size[0]}` and :math:`\text{kernel_size[1]}` are the height and width of the convolution kernel.
    The full kernel has shape :math:`(C_{out}, C_{in} / \text{group}, \text{kernel_size[0]}, \text{kernel_size[1]})`,
    where `group` is the group number to split the input in the channel dimension.

    If the `pad_mode` is set to be "valid", the output height and width will be :math:`\left \lfloor{
    1 + \frac{H_{in} + \text{padding[0]} + \text{padding[1]} - \text{kernel_size[0]} -
    (\text{kernel_size[0]} - 1) \times(\text{dilation[0]} - 1)} {\text { stride[0] }}} \right \rfloor` and

    :math:`\left \lfloor{1 + \frac{W_{in} + \text{padding[2]} + \text{padding[3]} - \text{kernel_size[1]} -
    (\text{kernel_size[1]} - 1) \times(\text{dilation[1]} - 1)} {\text { stride[1] }}} \right \rfloor` respectively.

    Where :math:`dilation` is Spacing between kernel elements, :math:`stride` is The step length of each step,
    :math:`padding` is zero-padding added to both sides of the input.
    For output height and width on other `pad_mode`, please refer to formula on `mindspore.nn.Conv2d
    <https://www.mindspore.cn/docs/en/r2.0.0-alpha/api_python/nn/mindspore.nn.Conv2d.html>`_.

    The first introduction can be found in paper `Gradient Based Learning Applied to Document Recognition
    <http://vision.stanford.edu/cs598_spring07/papers/Lecun98.pdf>`_. More detailed introduction can be found here:
    `ConvNets <http://cs231n.github.io/convolutional-networks/>`_ .

    Note:
        On Ascend platform, only group convolution in depthwise convolution scenarios is supported.
        That is, when `group>1`, condition `C_{in}` = `C_{out}` = `group` must be satisfied.

    Args:
        inputs (Tensor): Tensor of shape :math:`(N, C_{in}, H_{in}, W_{in})`.
        weight (Tensor): Set size of kernel is :math:`(\text{kernel_size[0]}, \text{kernel_size[1]})`,
            then the shape is :math:`(C_{out}, C_{in}, \text{kernel_size[0]}, \text{kernel_size[1]})`.
        pad_mode (str, optional): Specifies padding mode. The optional values are
            "same", "valid" and "pad". Default: "valid".

            - same: Adopts the way of completion. The height and width of the output will be equal to
              the input `x` divided by stride. The padding will be evenly calculated in top and bottom,
              left and right possiblily. Otherwise, the last extra padding will be calculated from the bottom
              and the right side. If this mode is set, `padding` must be 0.

            - valid: Adopts the way of discarding. The possible largest height and width of output will be returned
              without padding. Extra pixels will be discarded. If this mode is set, `padding` must be 0.

            - pad: Implicit paddings on both sides of the input `x`. The number of `padding` will be padded to the input
              Tensor borders. `padding` must be greater than or equal to 0.
        padding (Union(int, tuple[int]), optional): Implicit paddings on both sides of the input `x`.
            If `padding` is one integer, the paddings of top, bottom, left and right are the same, equal to padding.
            If `padding` is a tuple with four integers, the paddings of top, bottom, left and right will be equal
            to padding[0], padding[1], padding[2], and padding[3] accordingly. Default: 0.
        stride (Union(int, tuple[int]), optional): The distance of kernel moving, an int number that represents
            the height and width of movement are both strides, or a tuple of two int numbers that
            represent height and width of movement respectively. Default: 1.
        dilation (Union(int, tuple[int]), optional): The data type is int or a tuple of 2 integers.
            Specifies the dilation rate to use for dilated convolution. If set to be :math:`k > 1`, there will
            be :math:`k - 1` pixels skipped for each sampling location. Its value must
            be greater than or equal to 1 and bounded by the height and width of the input `x`. Default: 1.
        group (int, optional): Splits inputs into groups. Default: 1.

    Returns:
        Tensor, the value that applied 2D convolution. The shape is :math:`(N, C_{out}, H_{out}, W_{out})`.

    Raises:
        TypeError: If `stride`, `padding` or `dilation` is neither an int nor a tuple.
        TypeError: If `out_channel` or `group` is not an int.
        ValueError: If `stride` or `dilation` is less than 1.
        ValueError: If `pad_mode` is not one of 'same', 'valid' or 'pad'.
        ValueError: If `padding` is a tuple whose length is not equal to 4.
        ValueError: If `pad_mode` it not equal to 'pad' and `padding` is not equal to (0, 0, 0, 0).

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> x = Tensor(np.ones([10, 32, 32, 32]), mindspore.float32)
        >>> weight = Tensor(np.ones([32, 32, 3, 3]), mindspore.float32)
        >>> output = ops.conv2d(x, weight)
        >>> print(output.shape)
        (10, 32, 30, 30)
    """
    weight_shape = weight.shape
    out_channel = weight_shape[0]
    kernel_size = weight_shape[2:4]
    conv = _get_cache_prim(P.Conv2D)(out_channel, kernel_size, 1, pad_mode, padding, stride, dilation, group, "NCHW")
    output = conv(inputs, weight)
    return output


def hardsigmoid(input_x):
    r"""
    Hard sigmoid activation function.

    Applies hard sigmoid activation element-wise. The input is a Tensor with any valid shape.

    Hard sigmoid is defined as:

    .. math::

        \text{hsigmoid}(x_{i}) = max(0, min(1, \frac{x_{i} + 3}{6})),

    where :math:`x_i` is an element of the input Tensor.

    Inputs:
        - **input_x** (Tensor) - Tensor of shape :math:`(*)`, where :math:`*` means any number of
          dimensions, with float16, float32 or float64 data type.

    Outputs:
        A Tensor whose dtype and shape are the same as `input_x`.

    Raises:
        TypeError: If `input_x` is not a Tensor.
        TypeError: If dtype of `input_x` is not float16, float32 or float64.

    Supported Platforms:
        ``Ascend`` ``CPU``

    Examples:
        >>> x = Tensor(np.array([ -3.5,  0,  4.3]), mindspore.float32)
        >>> output = F.hardsigmoid(x)
        >>> print(output)
        [0.  0.5 1. ]
    """
    hardsigmoid_ = NN_OPS.HSigmoid()
    return hardsigmoid_(input_x)


def adaptive_avg_pool1d(input_x, output_size):
    r"""
    Applies a 1D adaptive average pooling over an input Tensor which can be regarded as a composition of 1D input
    planes.

    Typically, the input is of shape :math:`(N_{in}, C_{in}, L_{in})`, adaptive_avg_pool1d outputs regional average
    in the :math:`L_{in}`-dimension. The output is of shape :math:`(N_{in}, C_{in}, L_{out})`, where :math:`L_{out}`
    is defined by `output_size`.

    Note:
        :math:`L_{in}` must be divisible by `output_size`.

    Args:
        input_x (Tensor): Tensor of shape :math:`(N, C_{in}, L_{in})`, with float16 or float32 data type.
        output_size (int): the target output size :math:`L_{out}`.

    Returns:
        Tensor of shape :math:`(N, C_{in}, L_{out})`, has the same type as `input_x`.

    Raises:
        TypeError: If `output_size` is not an int.
        TypeError: If `input_x` is neither float16 nor float32.
        ValueError: If `output_size` is less than 1.
        ValueError: If length of shape of `input_x` is not equal to 3.
        ValueError: If the last dimension of `input_x` is smaller than `output_size`.
        ValueError: If the last dimension of `input_x` is not divisible by `output_size`.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> input_x = Tensor(np.random.randint(0, 10, [1, 3, 6]), mindspore.float32)
        >>> output = ops.adaptive_avg_pool1d(input_x, output_size=2)
        >>> print(output.shape)
        (1, 3, 2)
    """
    if not isinstance(input_x, (Tensor, Tensor_)):
        raise TypeError("For adaptive_avg_pool1d, the input input_x must be tensor")

    x_in_shape = input_x.shape
    x_dtype = _get_cache_prim(P.DType)()(input_x)

    validator.check_int(output_size, 1, Rel.GE, "output_size", 'adaptive_avg_pool1d')
    validator.check_value_type('output_size', output_size, [int], 'adaptive_avg_pool1d')

    if len(x_in_shape) != 3:
        raise ValueError("For adaptive_avg_pool1d input must have 3 dim, but got {}.".format(len(x_in_shape)))
    if x_in_shape[2] < output_size:
        raise ValueError("For adaptive_avg_pool1d input's last dimension must be greater or equal to "
                         "output size {}, but got {}.".format(output_size, x_in_shape[2]))
    if x_in_shape[2] % output_size != 0:
        raise ValueError("For adaptive_avg_pool1d input's last dimension must be divisible by "
                         "output size {}, but got {}.".format(output_size, x_in_shape[2]))
    if x_dtype not in [mstype.float16, mstype.float32]:
        raise TypeError("For adaptive_avg_pool1d, the input_x dtype must be float16 or float32, "
                        "but got {}.".format(x_dtype))

    expand_ = _get_cache_prim(P.ExpandDims)()
    squeeze_ = _get_cache_prim(P.Squeeze)(2)

    width = x_in_shape[2]
    stride = width // output_size
    kernel_size = width - (output_size - 1) * stride
    stride = (1, width // output_size)
    kernel_size = (1, kernel_size)

    avg_pool_ = _get_cache_prim(P.AvgPool)(kernel_size=kernel_size, strides=stride)

    input_x = expand_(input_x, 2)
    input_x = avg_pool_(input_x)
    input_x = squeeze_(input_x)

    return input_x


@constexpr
def _check_adaptive_max_pool1d_output_size(output_size):
    """Check the output_size value in adaptive_max_pool1d op."""
    validator.check_int(output_size, 1, Rel.GE, "output_size", 'adaptive_max_pool1d')
    validator.check_value_type('output_size', output_size, [int], 'adaptive_max_pool1d')


def adaptive_max_pool1d(input_x, output_size):
    r"""
    Applies a 1D adaptive maximum pooling over an input Tensor which can be regarded as
    a composition of 1D input planes.

    Typically, the input is of shape :math:`(N_{in}, C_{in}, L_{in})`,
    adaptive_max_pool1d outputs regional maximum in the :math:`L_{in}`-dimension. The output is of
    shape :math:`(N_{in}, C_{in}, L_{out})`, where :math:`L_{out}` is defined by `output_size`.

    Note:
        :math:`L_{in}` must be divisible by `output_size`.

    Args:
        input_x (Tensor): Tensor of shape :math:`(N, C_{in}, L_{in})`, with float16 or float32 data type.
        output_size (int): the target output size :math:`L_{out}`.

    Returns:
        Tensor of shape :math:`(N, C_{in}, L_{out})`, has the same type as `input_x`.

    Raises:
        TypeError: If `input_x` is neither float16 nor float32.
        TypeError: If `output_size` is not an int.
        ValueError: If `output_size` is less than 1.
        ValueError: If the last dimension of `input_x` is smaller than `output_size`.
        ValueError: If the last dimension of `input_x` is not divisible by `output_size`.
        ValueError: If length of shape of `input_x` is not equal to 3.


    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> input_x = Tensor(np.random.randint(0, 10, [1, 3, 6]), mindspore.float32)
        >>> output = ops.adaptive_max_pool1d(input_x, output_size=2)
        >>> print(output.shape)
        (1, 3, 2)
    """
    if not isinstance(input_x, (Tensor, Tensor_)):
        raise TypeError("For adaptive_max_pool1d, the input input_x must be tensor")

    _check_adaptive_max_pool1d_output_size(output_size)

    x_in_shape = input_x.shape
    x_dtype = _get_cache_prim(P.DType)()(input_x)

    if len(x_in_shape) != 3:
        raise ValueError("For adaptive_max_pool1d input must have 3 dim, but got {}.".format(len(x_in_shape)))
    if x_in_shape[2] < output_size:
        raise ValueError("For adaptive_max_pool1d input's last dimension must be greater or equal to "
                         "output size {}, but got {}.".format(output_size, x_in_shape[2]))
    if x_in_shape[2] % output_size != 0:
        raise ValueError("For adaptive_max_pool1d input's last dimension must be divisible by "
                         "output size {}, but got {}.".format(output_size, x_in_shape[2]))
    if x_dtype not in [mstype.float16, mstype.float32]:
        raise TypeError("For adaptive_max_pool1d, the input_x dtype must be float16 or float32, "
                        "but got {}.".format(x_dtype))

    expand_ = _get_cache_prim(P.ExpandDims)()
    squeeze_ = _get_cache_prim(P.Squeeze)(2)

    width = x_in_shape[2]
    stride = width // output_size
    kernel_size = width - (output_size - 1) * stride

    stride = (1, width // output_size)
    kernel_size = (1, kernel_size)

    max_pool_ = _get_cache_prim(P.MaxPool)(kernel_size=kernel_size, strides=stride)
    input_x = expand_(input_x, 2)
    input_x = max_pool_(input_x)
    input_x = squeeze_(input_x)

    return input_x


def batch_norm(input_x, running_mean, running_var, weight, bias, training=False, momentum=0.1, eps=1e-5):
    r"""
    Batch Normalization for input data and updated parameters.

    Batch Normalization is widely used in convolutional neural networks. This operation
    applies Batch Normalization over inputs to avoid internal covariate shift as described
    in the paper `Batch Normalization: Accelerating Deep Network Training by Reducing Internal
    Covariate Shift <https://arxiv.org/abs/1502.03167>`_. It rescales and recenters the
    features using a mini-batch of data and the learned parameters can be described
    in the following formula,

    .. math::

        y = \frac{x - mean}{\sqrt{variance + \epsilon}} * \gamma + \beta

    where :math:`\gamma` is `weight`, :math:`\beta` is `bias`, :math:`\epsilon` is `eps`, :math:`mean` is the
    mean of `input_x`, :math:`variance` is the variance of `input_x`.

    .. warning::
        - If this operation is used for inferring and output "reserve_space_1" and "reserve_space_2" are usable,
            then "reserve_space_1" and "reserve_space_2" have the same value as "mean" and "variance" respectively.
        - For Ascend 310, the result accuracy fails to reach 1‰ due to the square root instruction.

    Note:
        - If `training` is `False`, `weight`, `bias`, `running_mean` and `running_var` are Tensors.
        - If `training` is `True`, `weight`, `bias`, `running_mean` and `running_var` are Parameters.

    Args:
        input_x (Tensor): Tensor of shape :math:`(N, C)`, with float16 or float32 data type.
        running_mean (Union[Tensor, Parameter]): The shape :math:`(C,)`, has the same data type with `weight`.
        running_var (Union[Tensor, Parameter]): The shape :math:`(C,)`, has the same data type with `weight`.
        weight (Union[Tensor, Parameter]): The shape :math:`(C,)`, with float16 or float32 data type.
        bias (Union[Tensor, Parameter]): The shape :math:`(C,)`, has the same data type with `weight`.
        training (bool): If `training` is `True`, `mean` and `variance` are computed during training.
            If `training` is `False`, they're loaded from checkpoint during inference. Default: False.
        momentum (float): The hyper parameter to compute moving average for `running_mean` and `running_var`
            (e.g. :math:`new\_running\_mean = (1 - momentum) * running\_mean + momentum * current\_mean`).
            Momentum value must be `[0, 1]`. Default: 0.1.
        eps (float): A small value added for numerical stability. Default: 1e-5.

    Returns:
        output_x (Tensor) - The same type and shape as the `input_x`. The shape is :math:`(N, C)`.

    Raises:
        TypeError: If `training` is not a bool.
        TypeError: If dtype of `eps` or `momentum` is not float.
        TypeError: If `input_x`, `weight`, `bias`, `running_mean` or `running_var` is not a Tensor.
        TypeError: If dtype of `input_x`, `weight` is neither float16 nor float32.

    Supported Platforms:
        ``Ascend`` ``CPU`` ``GPU``

    Examples:
        >>> input_x = Tensor(np.ones([2, 2]), mindspore.float32)
        >>> running_mean = Tensor(np.ones([2]), mindspore.float32)
        >>> running_var = Tensor(np.ones([2]), mindspore.float32)
        >>> weight = Tensor(np.ones([2]), mindspore.float32)
        >>> bias = Tensor(np.ones([2]), mindspore.float32)
        >>> output = ops.batch_norm(input_x, running_mean, running_var, weight, bias)
        >>> print(output)
        [[1. 1.]
         [1. 1.]]
    """
    batch_norm_op = _get_cache_prim(P.BatchNorm)(is_training=training, epsilon=eps, momentum=momentum)
    output = batch_norm_op(input_x, weight, bias, running_mean, running_var)
    return output[0]


def bias_add(input_x, bias):
    r"""
    Returns the sum of the `input_x` and the `bias` Tensor. Before adding, the `bias` Tensor will be broadcasted to be
    consistent with the shape of the `input_x` Tensor.

    Args:
        input_x (Tensor): The input tensor. The shape can be 2-5 dimensions.
        bias (Tensor): The bias tensor, with shape :math:`(C)`. C must be the same as channel dimension C of `input_x`.

    Returns:
        Tensor, with the same shape and data type as `input_x`.

    Raises:
        TypeError: If `input_x` or `bias` is not a Tensor.
        TypeError: If dtype of `input_x` or `bias` is inconsistent.
        TypeError: If dimension of `input_x` is not in the range [2, 5].

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> input_x = Tensor(np.arange(6).reshape((2, 3)), mindspore.float32)
        >>> bias = Tensor(np.random.random(3).reshape((3)), mindspore.float32)
        >>> output = ops.bias_add(input_x, bias)
        >>> print(output.shape)
        (2, 3)
    """
    bias_add_op = _get_cache_prim(P.BiasAdd)(data_format="NCHW")
    return bias_add_op(input_x, bias)


def binary_cross_entropy(logits, labels, weight=None, reduction='mean'):
    r"""
    Computes the binary cross entropy between predictive value `logits` and target value `labels`.

    Set `logits` as :math:`x`, `labels` as :math:`y`, output as :math:`\ell(x, y)`, the
    weight of nth batch of binary cross entropy is :math:`w_n`.
    Let,

    .. math::
        L = \{l_1,\dots,l_N\}^\top, \quad
        l_n = - w_n \left[ y_n \cdot \log x_n + (1 - y_n) \cdot \log (1 - x_n) \right]

    In which, :math:`L` indicates the loss of all `batch_size`, :math:`l` indicates the loss of one `batch_size`,
    and :math:`n` indicates one `batch_size` in the :math:`1-N` range. Then,

    .. math::
        \ell(x, y) = \begin{cases}
        L, & \text{if reduction} = \text{'none';}\\
        \operatorname{mean}(L), & \text{if reduction} = \text{'mean';}\\
        \operatorname{sum}(L),  & \text{if reduction} = \text{'sum'.}
        \end{cases}

    .. warning::
        - The value of `logits` must range from `0` to `l`.
        - The value of `labels` must be `0` or `l`.

    Args:
        logits (Tensor): The predictive value whose data type must be float16 or float32.
            The shape is :math:`(N, *)` where :math:`*` means, any number of additional dimensions.
        labels (Tensor): The target value which has the same shape and data type as `logits`.
        weight (Tensor, optional): A rescaling weight applied to the loss of each batch element.
            Its shape must be able to broadcast to that of `logits` and `labels`.
            And it must have the same shape and data type as `logits`. Default: None.
        reduction (str): Specifies the reduction to be applied to the output.
            Its value must be one of 'none', 'mean' or 'sum', not case-sensitive. Default: 'mean'.

    Returns:
        Tensor or Scalar. Returns Tensor that has the same dtype and shape as `logits` if `reduction` is 'none'.
        Otherwise, returns a scalar Tensor.

    Raises:
        TypeError: If `logits`, `labels` or `weight` is not a Tensor.
        TypeError: If dtype of `logits`, `labels` or `weight` (if given) is neither float16 nor float32.
        ValueError: If `reduction` is not one of 'none', 'mean' or 'sum'.
        ValueError: If shape of `labels` is not the same as `logits` or `weight` (if given).

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> logits = Tensor(np.array([0.2, 0.7, 0.1]), mindspore.float32)
        >>> labels = Tensor(np.array([0., 1., 0.]), mindspore.float32)
        >>> weight = Tensor(np.array([1, 2, 2]), mindspore.float32)
        >>> output = ops.binary_cross_entropy(logits, labels, weight)
        >>> print(output)
        0.38240486
    """
    binary_cross_entropy_op = _get_cache_prim(P.BinaryCrossEntropy)(reduction=reduction)
    return binary_cross_entropy_op(logits, labels, weight)


def conv3d(inputs, weight, pad_mode="valid", padding=0, stride=1, dilation=1, group=1):
    r"""
    Applies a 3D convolution over an input tensor. The input tensor is typically of shape
    :math:`(N, C_{in}, D_{in}, H_{in}, W_{in})` and output shape
    :math:`(N, C_{out}, D_{out}, H_{out}, W_{out})`. Where :math:`N` is batch size, :math:`C` is channel number,
    :math:`D` is depth, :math:`H` is height, :math:`W` is width.
    the formula is defined as:

    .. math::
        \operatorname{out}\left(N_{i}, C_{\text {out}_j}\right)=\operatorname{bias}\left(C_{\text {out}_j}\right)+
        \sum_{k=0}^{C_{in}-1} ccor(\text {weight}\left(C_{\text {out}_j}, k\right),
        \operatorname{input}\left(N_{i}, k\right))

    where :math:`k` is kernel,
    :math:`ccor` is the `cross-correlation <https://en.wikipedia.org/wiki/Cross-correlation>`_ ,
    :math:`C_{in}` is the channel number of the input, :math:`out_{j}` corresponds to the jth channel of
    the output and :math:`j` is in the range of :math:`[0，C_{out}-1]`. :math:`\text{weight}(C_{\text{out}_j}, k)`
    is a convolution kernel slice with shape
    :math:`(\text{kernel_size[0]}, \text{kernel_size[1]}, \text{kernel_size[2]})`,
    where :math:`\text{kernel_size[0]}`, :math:`\text{kernel_size[1]}` and :math:`\text{kernel_size[2]}` are
    the depth, height and width of the convolution kernel respectively. :math:`\text{bias}` is the bias parameter
    and :math:`\text{X}` is the input tensor.
    The shape of full convolution kernel is
    :math:`(C_{out}, C_{in} / \text{group}, \text{kernel_size[0]}, \text{kernel_size[1]}, \text{kernel_size[2]})`,
    where `group` is the number of groups to split the input `x` in the channel dimension.

    For more details, please refers to the paper `Gradient Based Learning Applied to Document
    Recognition <http://vision.stanford.edu/cs598_spring07/papers/Lecun98.pdf>`_ .

    Note:
        On Ascend platform, only group convolution in depthwise convolution scenarios is supported.
        That is, when `group>1`, condition `C_{in}` = `C_{out}` = `group` must be satisfied.

    Args:
        inputs (Tensor): Tensor of shape :math:`(N, C_{in}, D_{in}, H_{in}, W_{in})`.
        weight (Tensor): Set size of kernel is :math:`(\text{kernel_size[0]}, \text{kernel_size[1]},
            \text{kernel_size[2]})`, then the shape is :math:`(C_{out}, C_{in}, \text{kernel_size[0]},
            \text{kernel_size[1]}, \text{kernel_size[1]})`.
        pad_mode (str, optional): Specifies padding mode. The optional values are
            "same", "valid" and "pad". Default: "valid".

            - same: Adopts the way of completion. The depth, height and width of the output will be equal to
              the input `x` divided by stride. The padding will be evenly calculated in head and tail, top and bottom,
              left and right directions possiblily.
              Otherwise, the last extra padding will be calculated from the tail, bottom and the right side.
              If this mode is set, `pad` must be 0.

            - valid: Adopts the way of discarding. The possible largest depth, height and width of output
              will be returned without padding. Extra pixels will be discarded. If this mode is set, `pad`
              must be 0.

            - pad: Implicit paddings on both sides of the input in depth, height and width. The number of `pad` will
              be padded to the input Tensor borders. `pad` must be greater than or equal to 0.

        padding (Union[int, tuple[int]], optional): The pad value to be filled. Default: 0. If `pad` is an integer,
            the paddings of head, tail, top, bottom, left and right are the same, equal to pad.
            If `pad` is a tuple of six integers, the padding of head, tail, top, bottom,
            left and right equal to pad[0], pad[1], pad[2], pad[3], pad[4] and pad[5] correspondingly.
        stride (Union[int, tuple[int]], optional): The distance of kernel moving, an int number that represents
            the height and width of movement are both strides, or a tuple of two int numbers that
            represent height and width of movement respectively. Default: 1.
        dilation (Union[int, tuple[int]], optional): The data type is int or a tuple of 3 integers
            :math:`(dilation_d, dilation_h, dilation_w)`. Currently, dilation on depth only supports the case of 1
            on Ascend backend. Specifies the dilation rate to use for dilated convolution. If set :math:`k > 1`,
            there will be :math:`k - 1` pixels skipped for each sampling location.
            Its value must be greater than or equal to 1 and bounded by the height and width of the input. Default: 1.
        group (int, optional): Splits filter into groups. Default: 1.

    Returns:
        Tensor, the value that applied 3D convolution. The shape is :math:`(N, C_{out}, D_{out}, H_{out}, W_{out})`.

        `pad_mode` is 'same':

        .. math::
            \begin{array}{ll} \\
                D_{out} ＝ \left \lceil{\frac{D_{in}}{\text{stride[0]}}} \right \rceil \\
                H_{out} ＝ \left \lceil{\frac{H_{in}}{\text{stride[1]}}} \right \rceil \\
                W_{out} ＝ \left \lceil{\frac{W_{in}}{\text{stride[2]}}} \right \rceil \\
            \end{array}

        `pad_mode` is 'valid':

        .. math::
            \begin{array}{ll} \\
                D_{out} ＝ \left \lfloor{\frac{D_{in} - \text{dilation[0]} \times (\text{kernel_size[0]} - 1) }
                {\text{stride[0]}} + 1} \right \rfloor \\
                H_{out} ＝ \left \lfloor{\frac{H_{in} - \text{dilation[1]} \times (\text{kernel_size[1]} - 1) }
                {\text{stride[1]}} + 1} \right \rfloor \\
                W_{out} ＝ \left \lfloor{\frac{W_{in} - \text{dilation[2]} \times (\text{kernel_size[2]} - 1) }
                {\text{stride[2]}} + 1} \right \rfloor \\
            \end{array}

        `pad_mode` is 'pad':

        .. math::
            \begin{array}{ll} \\
                D_{out} ＝ \left \lfloor{\frac{D_{in} + padding[0] + padding[1] - (\text{dilation[0]} - 1) \times
                \text{kernel_size[0]} - 1 }{\text{stride[0]}} + 1} \right \rfloor \\
                H_{out} ＝ \left \lfloor{\frac{H_{in} + padding[2] + padding[3] - (\text{dilation[1]} - 1) \times
                \text{kernel_size[1]} - 1 }{\text{stride[1]}} + 1} \right \rfloor \\
                W_{out} ＝ \left \lfloor{\frac{W_{in} + padding[4] + padding[5] - (\text{dilation[2]} - 1) \times
                \text{kernel_size[2]} - 1 }{\text{stride[2]}} + 1} \right \rfloor \\
            \end{array}

    Raises:
        TypeError: If `out_channel` or `group` is not an int.
        TypeError: If `stride`, `padding` or `dilation` is neither an int nor a tuple.
        ValueError: If `stride` or `dilation` is less than 1.
        ValueError: If `pad_mode` is not one of 'same', 'valid' or 'pad'.
        ValueError: If `padding` is a tuple whose length is not equal to 4.
        ValueError: If `pad_mode` is not equal to 'pad' and `pad` is not equal to (0, 0, 0, 0, 0, 0).

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> x = Tensor(np.ones([16, 3, 10, 32, 32]), mindspore.float16)
        >>> weight = Tensor(np.ones([32, 3, 4, 3, 3]), mindspore.float16)
        >>> output = ops.conv3d(x, weight)
        >>> print(output.shape)
        (16, 32, 7, 30, 30)
    """
    weight_shape = weight.shape
    out_channel = weight_shape[0]
    kernel_size = weight_shape[2:5]
    conv = _get_cache_prim(P.Conv3D)(out_channel, kernel_size, 1, pad_mode, padding, stride, dilation, group, "NCDHW")
    output = conv(inputs, weight)
    return output


@constexpr
def _check_positive_int(arg_value, arg_name=None, prim_name=None):
    validator.check_positive_int(arg_value, arg_name=arg_name, prim_name=prim_name)


def pixel_shuffle(x, upscale_factor):
    r"""
    Applies a pixel_shuffle operation over an input signal composed of several input planes. This is useful for
    implementiong efficient sub-pixel convolution with a stride of :math:`1/r`. For more details, refer to
    `Real-Time Single Image and Video Super-Resolution Using an Efficient Sub-Pixel Convolutional Neural Network
    <https://arxiv.org/abs/1609.05158>`_ .

    Typically, the `x` is of shape :math:`(*, C \times r^2, H, W)` , and the output is of shape
    :math:`(*, C, H \times r, W \times r)`, where `r` is an upscale factor and `*` is zero or more batch dimensions.

    Args:
        x (Tensor): Tensor of shape :math:`(*, C \times r^2, H, W)` . The dimension of `x` is larger than 2, and the
            length of third to last dimension can be divisible by `upscale_factor` squared.
        upscale_factor (int):  factor to increase spatial resolution by, and is a positive integer.

    Returns:
        - **output** (Tensor) - Tensor of shape :math:`(*, C, H \times r, W \times r)` .

    Raises:
        ValueError: If `upscale_factor` is not a positive integer.
        ValueError: If the length of third to last dimension is not divisible by `upscale_factor` squared.
        TypeError: If the dimension of `x` is less than 3.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> input_x = np.arange(3 * 2 * 9 * 4 * 4).reshape((3, 2, 9, 4, 4))
        >>> input_x = mindspore.Tensor(input_x, mindspore.dtype.int32)
        >>> output = ops.pixel_shuffle(input_x, 3)
        >>> print(output.shape)
        (3, 2, 1, 12, 12)
    """
    _check_positive_int(upscale_factor, "upscale_factor")
    idx = x.shape
    length = len(idx)
    if length < 3:
        raise TypeError(f"For pixel_shuffle, the dimension of `x` should be larger than 2, but got {length}.")
    pre = idx[:-3]
    c, h, w = idx[-3:]
    if c % upscale_factor ** 2 != 0:
        raise ValueError("For 'pixel_shuffle', the length of third to last dimension is not divisible"
                         "by `upscale_factor` squared.")
    c = c // upscale_factor ** 2
    input_perm = (pre + (c, upscale_factor, upscale_factor, h, w))
    reshape = ops.Reshape()
    x = reshape(x, input_perm)
    input_perm = [i for i in range(length - 2)]
    input_perm = input_perm + [length, length - 2, length + 1, length - 1]
    input_perm = tuple(input_perm)
    transpose = ops.Transpose()
    x = transpose(x, input_perm)
    x = reshape(x, (pre + (c, upscale_factor * h, upscale_factor * w)))
    return x


def pixel_unshuffle(x, downscale_factor):
    r"""
    Applies a pixel_unshuffle operation over an input signal composed of several input planes. For more details, refer
    to `Real-Time Single Image and Video Super-Resolution Using an Efficient Sub-Pixel Convolutional Neural Network
    <https://arxiv.org/abs/1609.05158>`_ .

    Typically, the input is of shape :math:`(*, C, H \times r, W \times r)` , and the output is of shape
    :math:`(*, C \times r^2, H, W)` , where `r` is a downscale factor and `*` is zero or more batch dimensions.

    Args:
        x (Tensor): Tensor of shape :math:`(*, C, H \times r, W \times r)` . The dimension of `x` is larger than 2,
            and the length of second to last dimension or last dimension can be divisible by `downscale_factor` .
        downscale_factor (int): factor to decrease spatial resolution by, and is a positive integer.

    Returns:
        - **output** (Tensor) - Tensor of shape :math:`(*, C \times r^2, H, W)` .

    Raises:
        ValueError: If `downscale_factor` is not a positive integer.
        ValueError: If the length of second to last dimension or last dimension is not divisible by `downscale_factor` .
        TypeError: If the dimension of `x` is less than 3.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> input_x = np.arange(12 * 12).reshape((1, 1, 12, 12))
        >>> input_x = mindspore.Tensor(input_x, mindspore.dtype.int32)
        >>> output = ops.pixel_unshuffle(input_x, 3)
        >>> print(output.shape)
        (1, 9, 4, 4)
    """
    _check_positive_int(downscale_factor, "downscale_factor")
    idx = x.shape
    length = len(idx)
    if length < 3:
        raise TypeError(f"For pixel_unshuffle, the dimension of `x` should be larger than 2, but got {length}.")
    pre = idx[:-3]
    c, h, w = idx[-3:]
    if h % downscale_factor != 0 or w % downscale_factor != 0:
        raise ValueError("For 'pixel_unshuffle', the length of second to last 2 dimension should be divisible "
                         "by downscale_factor.")
    h = h // downscale_factor
    w = w // downscale_factor
    input_perm = (pre + (c, h, downscale_factor, w, downscale_factor))
    reshape = ops.Reshape()
    x = reshape(x, input_perm)
    input_perm = [i for i in range(length - 2)]
    input_perm = input_perm + [length - 1, length + 1, length - 2, length]
    input_perm = tuple(input_perm)
    transpose = ops.Transpose()
    x = transpose(x, input_perm)
    x = reshape(x, (pre + (c * downscale_factor * downscale_factor, h, w)))
    return x


def glu(x, axis=-1):
    r"""
    Computes GLU (Gated Linear Unit activation function) of input tensors .

    .. math::
        {GLU}(a, b)= a \otimes \sigma(b)

    where :math:`a` is the first half of the input matrices and :math:`b` is the second half.

    Here :math:`\sigma` is the sigmoid function, and :math:`*` is the Hadamard product.
    See `Language Modeling with Gated Convluational Networks <https://arxiv.org/abs/1612.08083>`_.

    Args:
        x (Tensor): Tensor to be splited. Its dtype is number.Number, and shape is :math:`(\ast_1, N, \ast_2)`
            where `*` means, any number of additional dimensions.
        axis (int, optional): the dimension on which to split the input. It must be int. Default: -1.

    Returns:
        Tensor, the same dtype as the `x`, with the shape :math:`(\ast_1, M, \ast_2)` where :math:`M=N/2`.

    Raises:
        TypeError: If dtype of `x` is not number.Number.
        TypeError: If `x` is not a Tensor.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> input = Tensor([[0.1,0.2,0.3,0.4],[0.5,0.6,0.7,0.8]])
        >>> output = ops.glu(input)
        >>> print(output)
        [[0.05744425 0.11973753]
         [0.33409387 0.41398472]]
    """
    if not isinstance(x, Tensor) or x.size == 0:
        raise TypeError("glu does not support scalars because halving size must be even")

    spilt = _get_cache_prim(P.Split)(axis=axis, output_num=2)
    x, y = spilt(x)
    y = sigmoid_(y)
    return x * y


def multi_margin_loss(inputs, target, p=1, margin=1, weight=None, reduction='mean'):
    r"""
    Hinge loss for optimizing a multi-class classification.

    Creates a criterion that optimizes a multi-class classification hinge
    loss (margin-based loss) between input :math:`x` (a 2D mini-batch `Tensor`) and
    output :math:`y` (which is a 1D tensor of target class indices,
    :math:`0 \leq y \leq \text{x.size}(1)-1`):
    For each mini-batch sample, the loss in terms of the 1D input :math:`x` and scalar
    output :math:`y` is:

    .. math::
        \text{loss}(x, y) = \frac{\sum_i \max(0, w[y] * (\text{margin} - x[y] + x[i]))^p)}{\text{x.size}(0)}

    where :math:`x \in \left\{0, \; \cdots , \; \text{x.size}(0) - 1\right\}`
    and :math:`i \neq y`.
    Optionally, you can give non-equal weighting on the classes by passing
    a 1D input `weight` tensor into the constructor.

    Args:
        inputs (Tensor): Input , with shape :math:`(N, C)`. Data type only support float32, float16 or float64.
        target (Tensor): Ground truth labels, with shape :math:`(N,)`. Data type only support int64. The
            value of target should be non-negative, less than C.
        p (int, optional): The norm degree for pairwise distance. Should be 1 or 2. Default: 1.
        margin (int, optional): A parameter to change pairwise distance. Default: 1.
        weight (Tensor, optional): The rescaling weight to each class with shape :math:`(C,)`. Data type only
            support float16, float32 or float64. Default: None.
        reduction (str, optional): Apply specific reduction method to the output: 'none', 'mean',
            'sum'. Default: 'mean'.

            - 'none': no reduction will be applied.
            - 'mean': the sum of the output will be divided by the number of elements in the output.
            - 'sum': the output will be summed.

    Returns:
        Tensor, When `reduction` is 'none', the shape is :math:`(N,)`.
        Otherwise, it is a scalar. Has the same data type with `inputs`.

    Raises:
        TypeError: If dtype of `p` or `target` is not int.
        TypeError: If dtype of `margin` is not int.
        TypeError: If dtype of `reduction` is not str.
        TypeError: If dtype of `inputs` is not float16, float or float64.
        TypeError: If dtype of `weight` and `inputs` is not the same.
        ValueError: If `p` is not 1 or 2.
        ValueError: If `reduction` is not one of {'none','sum','mean'}.
        ValueError: If shape[0] of `inputs` is not equal to shape[0] of `target`.
        ValueError: If shape[1] of `inputs` is not equal to shape[0] of `weight`.
        ValueError: If rank of `weight` is not 1 or  rank of `target` is not 1 or `inputs` is not 2.

    Supported Platforms:
        ``Ascend``  ``CPU``

    Examples:
        >>> inputs = Tensor(np.ones(shape=[3, 3]), mindspore.float32)
        >>> target = Tensor(np.array([1, 2, 1]), mindspore.int64)
        >>> weight = Tensor(np.array([1, 1, 1]), mindspore.float32)
        >>> output = ops.multi_margin_loss(inputs, target, weight=weight)
        >>> print(output)
        0.6666667
    """

    if not isinstance(margin, int):
        raise TypeError(f"For 'multi_margin_loss', the type of 'margin' must be int, but got {type(margin)}.")
    margin_ = float(margin)
    loss = _get_cache_prim(P.MultiMarginLoss)(p, margin_, reduction)
    outputs = loss(inputs, target, weight)
    return outputs


def multi_label_margin_loss(inputs, target, reduction='mean'):
    r"""
    Hinge loss for optimizing a multi-label classification.

    Creates a criterion that optimizes a multi-label multi-classification
    hinge loss (margin-based loss) between input :math:`x` (a 2D mini-batch `Tensor`)
    and output :math:`y` (which is a 2D `Tensor` of target class indices).
    For each sample in the mini-batch:

    .. math::
        \text{loss}(x, y) = \sum_{ij}\frac{\max(0, 1 - (x[y[j]] - x[i]))}{\text{x.size}(0)}

    where :math:`x \in \left\{0, \; \cdots , \; \text{x.size}(0) - 1\right\}`, \
    :math:`y \in \left\{0, \; \cdots , \; \text{y.size}(0) - 1\right\}`, \
    :math:`0 \leq y[j] \leq \text{x.size}(0)-1`, \
    and :math:`i \neq y[j]` for all :math:`i` and :math:`j`.
    :math:`y` and :math:`x` must have the same size.
    The criterion only considers a contiguous block of non-negative targets that
    starts at the front.
    This allows for different samples to have variable amounts of target classes.

    Args:
        inputs (Tensor): Predict data. Tensor of shape :math:`(C)` or :math:`(N, C)`, where :math:`N`
            is the batch size and :math:`C` is the number of classes. Data type must be float16 or float32.
        target (Tensor): Ground truth data, with the same shape as `inputs`, data type must be int32 and
            label targets padded by -1.
        reduction (str, optional): Apply specific reduction method to the output: 'none', 'mean',
            'sum'. Default: 'mean'.

            - 'none': no reduction will be applied.
            - 'mean': the sum of the output will be divided by the number of elements in the output.
            - 'sum': the output will be summed.

    Returns:
        - **outputs** (Union[Tensor, Scalar]) - The loss of MultilabelMarginLoss. If `reduction` is "none", its shape
          is :math:`(N)`. Otherwise, a scalar value will be returned.


    Raises:
        TypeError: If `inputs` or `target` is not a Tensor.
        TypeError: If dtype of `inputs` is neither float16 nor float32.
        TypeError: If dtype of `target` is not int32.
        ValueError: If length of shape of `inputs` is neither 1 nor 2.
        ValueError: If shape of `inputs` is not the same as `target`.
        ValueError: If `reduction` is not one of 'none', 'mean', 'sum'.

    Supported Platforms:
        ``Ascend`` ``GPU``

    Examples:
       >>> inputs = Tensor(np.array([[0.1, 0.2, 0.4, 0.8], [0.2, 0.3, 0.5, 0.7]]), mindspore.float32)
       >>> target = Tensor(np.array([[1, 2, 0, 3], [2, 3, -1, 1]]), mindspore.int32)
       >>> output, _ = ops.multi_label_margin_loss(inputs, target)
       >>> print(output)
       (Tensor(shape=[], dtype=Float32, value= 0.325), Tensor(shape=[2, 4], dtype=Int32, value=
       [[1, 1, 1, 1], [0, 0, 1, 1]]))
    """

    loss = _get_cache_prim(P.MultilabelMarginLoss)(reduction)
    outputs, _ = loss(inputs, target)
    return outputs


def elu(input_x, alpha=1.0):
    r"""
    Exponential Linear Unit activation function.

    Applies the exponential linear unit function element-wise.
    The activation function is defined as:

    .. math::

        \text{ELU}(x)= \left\{
        \begin{array}{align}
            \alpha(e^{x}  - 1) & \text{if } x \le 0\\
            x & \text{if } x \gt 0\\
        \end{array}\right.

    Where :math:`x` is the element of input Tensor `input_x`, :math:`\alpha` is param `alpha`,
    it determines the smoothness of ELU.
    The picture about ELU looks like this `ELU <https://en.wikipedia.org/wiki/
    Activation_function#/media/File:Activation_elu.svg>`_ .

    Args:
        input_x (Tensor): The input of ELU is a Tensor of any dimension with data type of float16 or float32.
        alpha (float): The alpha value of ELU, the data type is float. Only support '1.0' currently. Default: 1.0.

    Returns:
        Tensor, has the same shape and data type as `input_x`.

    Raises:
        TypeError: If `alpha` is not a float.
        TypeError: If dtype of `input_x` is neither float16 nor float32.
        ValueError: If `alpha` is not equal to 1.0.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> x = Tensor(np.array([[-1.0, 4.0, -8.0], [2.0, -5.0, 9.0]]), mindspore.float32)
        >>> output = ops.elu(x)
        >>> print(output)
        [[-0.63212055  4.         -0.99966455]
         [ 2.         -0.99326205  9.        ]]
    """
    return _get_cache_prim(P.Elu)(alpha=alpha)(input_x)


def gelu(input_x, approximate='none'):
    r"""
    Gaussian Error Linear Units activation function.

    GeLU is described in the paper `Gaussian Error Linear Units (GELUs) <https://arxiv.org/abs/1606.08415>`_.
    And also please refer to `BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding
    <https://arxiv.org/abs/1810.04805>`_.

    When `approximate` argument is `none`, GeLU is defined as follows:

    .. math::
        GELU(x_i) = x_i*P(X < x_i)

    where :math:`P` is the cumulative distribution function of the standard Gaussian distribution,
    :math:`x_i` is the input element.

    When `approximate` argument is `tanh`, GeLU is estimated with:

    .. math::
        GELU(x_i) = 0.5 * x_i * (1 + tanh(\sqrt(2 / \pi) * (x_i + 0.044715 * x_i^3)))

    Args:
        input_x (Tensor): The input of the activation function GeLU, the data type is float16, float32 or float64.
        approximate (str): the gelu approximation algorithm to use. Acceptable vaslues are 'none' and 'tanh'.
            Default: 'none'.

    Returns:
        Tensor, with the same type and shape as `input_x`.

    Raises:
        TypeError: If `input_x` is not a Tensor.
        TypeError: If dtype of `input_x` is not float16, float32 or float64.
        ValueError: If `approximate` value is neither `none` or `tanh`.

    Supported Platforms:
        ``Ascend`` ``CPU`` ``GPU``

    Examples:
        >>> x = Tensor([1.0, 2.0, 3.0], mindspore.float32)
        >>> result = ops.gelu(x)
        >>> print(result)
        [0.841192 1.9545976 2.9963627]
    """
    if approximate not in ['none', 'tanh']:
        raise ValueError("For ops.gelu, approximate value should be either 'none' or 'tanh'.")

    output = _get_cache_prim(P.GeLU)()(input_x)

    if approximate == 'tanh':
        output = _get_cache_prim(P.Pow)()(input_x, Tensor([3]))
        output = output * Tensor([0.044715]) + input_x
        output = output * _get_cache_prim(P.Sqrt)()(Tensor(2.0 / pi))
        output = _get_cache_prim(P.Tanh)()(output) + Tensor([1.0])
        output = output * input_x * Tensor([0.5])

    return output


@constexpr
def _shape_check(in_shape, dim_list, prim_name=None):
    msg_prefix = f"For '{prim_name}', the" if prim_name else "The"
    if len(in_shape) not in dim_list:
        raise ValueError(f"{msg_prefix} input must has dim in {dim_list}, but got {len(in_shape)}")


def lp_pool1d(x, norm_type, kernel_size, stride=None, ceil_mode=False):
    r"""
    Applies a 1D power lp pooling over an input signal composed of several input planes.

    Typically the input is of shape :math:`(N, C, L_{in})` or :math:`(C, L_{in})`, the output is of shape
    :math:`(N, C, L_{in})` or :math:`(C, L_{in})`, with the same shape as input, the operation is as follows.

    .. math::
        f(X) = \sqrt[p]{\sum_{x \in X} x^{p}}

    Args:
        x (Tensor): Tensor of shape :math:`(N, C, L_{in})` or :math:`(C, L_{in})`.
        norm_type (Union[int, float]): Type of normalization, represents p in the formula, can not be 0,

            - if p = 1, one gets Sum Pooling (which is proportional to Average Pooling),
            - if p = :math:`\infty`, one gets Max Pooling.

        kernel_size (int): The size of kernel window.
        stride (int): The distance of kernel moving, an int number that represents
            the width of movement is stride, if the value is None, the default value `kernel_size` is used;
        ceil_mode (bool): Whether to use ceil or floor to calculate output shape. Default: False.

    Returns:
        - **output** (Tensor) - LPPool1d result, with shape :math:`(N, C, L_{in})` or :math:`(C, L_{in})`,
          It has the same data type as `x`.

    Raises:
        TypeError: If `x` is not an Tensor.
        TypeError: If `kernel_size` or `stride` is not an int.
        TypeError: If `ceil_mode` is not a bool.
        TypeError: If `norm_type` is neither float nor int.
        ValueError: If `norm_type` is equal to 0.
        ValueError: If `kernel_size` or `stride` is less than 1.
        ValueError: If length of shape of `x` is not equal to 2 or 3.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> import mindspore as ms
        >>> import mindspore.ops as ops
        >>> from mindspore import Tensor
        >>> import numpy as np
        >>> x = Tensor(np.arange(2 * 3 * 4).reshape((2, 3, 4)), dtype=ms.float32)
        >>> out = ops.lp_pool1d(x, norm_type=1, kernel_size=3, stride=1, ceil_mode=False)
        >>> print(out)
        [[[ 3.  6.]
          [15. 18.]
          [27. 30.]]
         [[39. 42.]
          [51. 54.]
          [63. 66.]]]
    """
    _shape_check(x.shape, [2, 3], "lp_pool1d")
    if isinstance(norm_type, (float, int)):
        norm_type = float(norm_type)
    else:
        raise TypeError(f"For lp_pool1d, the type of 'norm_type' must be float or int, but got {type(norm_type)}")
    if norm_type == 0:
        raise ValueError(f"For lp_pool1d, the value of 'norm_type' can not be 0.")
    sign = _get_cache_prim(ops.Sign)()
    squeeze = _get_cache_prim(ops.Squeeze)(0)
    expand_dims = _get_cache_prim(ops.ExpandDims)()
    _is_squeeze = False
    if len(x.shape) == 2:
        x = expand_dims(x, 0)
        _is_squeeze = True
    if stride is not None:
        out = ops.avg_pool1d(x.pow(norm_type), kernel_size=kernel_size, stride=stride, padding=0, ceil_mode=ceil_mode)
    else:
        out = ops.avg_pool1d(x.pow(norm_type), kernel_size=kernel_size, stride=kernel_size, padding=0,
                             ceil_mode=ceil_mode)
    if _is_squeeze:
        out = squeeze(out)
    return ((sign(out) * ops.relu(ops.abs(out))) * kernel_size).pow(1.0 / norm_type)


def lp_pool2d(x, norm_type, kernel_size, stride=None, ceil_mode=False):
    r"""
    Applies a 2D power lp pooling over an input signal composed of several input planes.

    Typically the input is of shape :math:`(N, C, H_{in}, W_{in})`, the output is of shape
    :math:`(N, C, H_{in}, W_{in})`, with the same shape as input, the operation is as follows.

    .. math::
        f(X) = \sqrt[p]{\sum_{x \in X} x^{p}}

    Args:
        x (Tensor): Tensor of shape :math:`(N, C, H_{in}, W_{in})`.
        norm_type (Union[int, float]): Type of normalization, represents p in the formula, can not be 0,

            - if p = 1, one gets Sum Pooling (which is proportional to Average Pooling),
            - if p = :math:`\infty`, one gets Max Pooling.

        kernel_size (Union[int, tuple[int]]): The size of kernel window.
            The data type of kernel_size must be int and the value represents the height and width,
            or a tuple of two int numbers that represent height and width respectively.
        stride (Union[int, tuple[int]]): The distance of kernel moving, an int number that represents
            the height and width of movement are both strides, or a tuple of two int numbers that
            represent height and width of movement respectively, if the value is None,
            the default value `kernel_size` is used;
        ceil_mode (bool): Whether to use ceil or floor to calculate output shape. Default: False.

    Returns:
        - **output** (Tensor) - LPPool2d result, with shape :math:`(N, C, H_{in}, W_{in})`,
          It has the same data type as `x`.

    Raises:
        TypeError: If `x` is not an Tensor.
        TypeError: If `kernel_size` or `stride` is neither int nor tuple.
        TypeError: If `ceil_mode` is not a bool.
        TypeError: If `norm_type` is neither float nor int.
        ValueError: If `norm_type` is equal to 0.
        ValueError: If `kernel_size` or `stride` is less than 1.
        ValueError: If `kernel_size` or `stride` is a tuple whose length is not equal to `2`.
        ValueError: If length of shape of `x` is not equal to 4.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> import mindspore as ms
        >>> import mindspore.ops as ops
        >>> from mindspore import Tensor
        >>> import numpy as np
        >>> x = Tensor(np.arange(2 * 3 * 4 * 5).reshape((2, 3, 4, 5)), dtype=ms.float32)
        >>> out = ops.lp_pool2d(x, norm_type=1, kernel_size=3, stride=1, ceil_mode=False)
        >>> print(out)
        [[[[  54.   63.   72.]
           [  99.  108.  117.]]
          [[ 234.  243.  252.]
           [ 279.  288.  297.]]
          [[ 414.  423.  432.]
           [ 459.  468.  477.]]]
         [[[ 594.  603.  612.]
           [ 639.  648.  657.]]
          [[ 774.  783.  792.]
           [ 819.  828.  837.]]
          [[ 954.  963.  972.]
           [ 999. 1008. 1017.]]]]

    """
    _shape_check(x.shape, [4], "lp_pool2d")
    if isinstance(norm_type, (float, int)):
        norm_type = float(norm_type)
    else:
        raise TypeError(f"For lp_pool2d, the type of 'norm_type' must be float or int, but got {type(norm_type)}")
    if norm_type == 0:
        raise ValueError(f"For lp_pool2d, the value of 'norm_type' can not be 0.")
    sign = _get_cache_prim(ops.Sign)()
    if not isinstance(x, tuple):
        kernel_size = tuple((kernel_size, kernel_size))
    kw, kh = kernel_size
    if stride is not None:
        out = ops.avg_pool2d(x.pow(norm_type), kernel_size=kernel_size, stride=stride, padding=0, ceil_mode=ceil_mode)
    else:
        out = ops.avg_pool2d(x.pow(norm_type), kernel_size=kernel_size, stride=kernel_size, padding=0,
                             ceil_mode=ceil_mode)
    return ((sign(out) * ops.relu(ops.abs(out))) * (kw * kh)).pow(1.0 / norm_type)


def mse_loss(input_x, target, reduction='mean'):
    r"""
    Calculates the mean squared error between the predicted value and the label value.

    For detailed information, please refer to :class:`mindspore.nn.MSELoss`.

    Args:
        input_x (Tensor): Tensor of any dimension.
        target (Tensor): The input label. Tensor of any dimension, same shape as the `input_x` in common cases.
            However, it supports that the shape of `input_x` is different from the shape of `target`
            and they should be broadcasted to each other.
        reduction (str, optional): Type of reduction to be applied to loss.
            The optional values are "mean", "none" and "sum". Default: "mean".

    Returns:
        Tensor, loss of type float, the shape is zero if `reduction` is 'mean' or 'sum',
        while the shape of output is the broadcasted shape if `reduction` is 'none'.

    Raises:
        ValueError: If `reduction` is not one of 'none', 'mean' or 'sum'.
        ValueError: If `input_x` and `target` have different shapes and cannot be broadcasted.

    Supported Platforms:
        ``Ascend`` ``CPU`` ``GPU``

    Examples:
        >>> logits = Tensor(np.array([1, 2, 3]), mindspore.float32)
        >>> labels = Tensor(np.array([[1, 1, 1], [1, 2, 2]]), mindspore.float32)
        >>> output = ops.mse_loss(logits, labels, reduction='none')
        >>> print(output)
        [[0. 1. 4.]
         [0. 0. 1.]]
    """
    if not isinstance(input_x, (Tensor, Tensor_)):
        raise TypeError("For ops.mse_loss, the `input_x` must be tensor")
    if not isinstance(target, (Tensor, Tensor_)):
        raise TypeError("For ops.mse_loss, the `target` must be tensor")
    if reduction not in ['mean', 'none', 'sum']:
        raise ValueError("For ops.mse_loss, `reduction` value should be either 'mean', 'none' or 'sum'.")

    x = _get_cache_prim(P.Square)()(input_x - target)
    input_dtype = x.dtype
    x = _get_cache_prim(P.Cast)()(x, mstype.float32)

    average_flag = True
    reduce_flag = True
    if reduction == 'sum':
        average_flag = False
    if reduction == 'none':
        reduce_flag = False

    perm = _get_cache_prim(P.Range)()(Tensor(0, mstype.int32),
                                      Tensor(len(x.shape), mstype.int32),
                                      Tensor(1, mstype.int32))

    if reduce_flag and average_flag:
        x = _get_cache_prim(P.ReduceMean)()(x, perm)

    if reduce_flag and not average_flag:
        x = _get_cache_prim(P.ReduceSum)()(x, perm)

    return _get_cache_prim(P.Cast)()(x, input_dtype)


__all__ = [
    'adaptive_avg_pool1d',
    'adaptive_avg_pool2d',
    'adaptive_avg_pool3d',
    'adaptive_max_pool1d',
    'adaptive_max_pool2d',
    'adaptive_max_pool3d',
    'avg_pool1d',
    'avg_pool2d',
    'avg_pool3d',
    'batch_norm',
    'bias_add',
    'binary_cross_entropy',
    'binary_cross_entropy_with_logits',
    'max_pool3d',
    'kl_div',
    'celu',
    'deformable_conv2d',
    'dropout1d',
    'dropout2d',
    'dropout3d',
    'fast_gelu',
    'fractional_max_pool2d',
    'fractional_max_pool3d',
    'pixel_shuffle',
    'pixel_unshuffle',
    'hardshrink',
    'soft_shrink',
    'is_floating_point',
    'flip',
    'fliplr',
    'flipud',
    'intopk',
    'interpolate',
    'log_softmax',
    'mish',
    'lrn',
    'hardswish',
    'softsign',
    'selu',
    'softmax',
    'pdist',
    'pad',
    'prelu',
    'mirror_pad',
    'cross_entropy',
    'grid_sample',
    'smooth_l1_loss',
    'nll_loss',
    'ctc_loss',
    'ctc_greedy_decoder',
    'dropout',
    'conv3d_transpose',
    'conv2d',
    'sigmoid',
    'relu',
    'relu6',
    'conv3d',
    'glu',
    'margin_ranking_loss',
    'multi_margin_loss',
    'multi_label_margin_loss',
    'elu',
    'gelu',
    'hinge_embedding_loss',
    'gaussian_nll_loss',
    'lp_pool1d',
    'lp_pool2d',
    'max_unpool1d',
    'max_unpool2d',
    'max_unpool3d',
    'mse_loss',
]
__all__.sort()
